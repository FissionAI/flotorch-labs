import math
import pandas as pd

MILLION = 1_000_000
THOUSAND = 1_000
SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60
# Read the CSV file into a pandas DataFrame
df = pd.read_csv('./data/bedrock_limits_small.csv')


def calculate_experiment_question_details(experiment_question_metrics_items):
    total_questions = len(experiment_question_metrics_items)
    overall_inferencer_time = 0
    average_inferencer_time = 0
    reranker_queries = 0
    for question in experiment_question_metrics_items:
        answer_metadata = question.get("answer_metadata", None)
        if answer_metadata:
            latency = answer_metadata.get("latencyMs", 0)
            inputTokens = answer_metadata.get('inputTokens', 0)
            overall_inferencer_time += (latency / THOUSAND)
            if math.ceil(inputTokens / 500) >= 100:
                reranker_queries += (math.ceil(inputTokens / 500) / 100)
            else:
                reranker_queries += 1
    average_inferencer_time = overall_inferencer_time / total_questions
    return {
        "total_questions": total_questions,
        "overall_inferencer_time": overall_inferencer_time,
        "average_inferencer_time": average_inferencer_time,
        "reranker_queries": reranker_queries
    }

def calculate_bedrock_inference_cost(sample_input, exp_config_data):
    input_tokens = sample_input.get("answer_metadata", 0).get("inputTokens", 0)
    output_tokens = sample_input.get("answer_metadata", 0).get("outputTokens", 0)

    retrieval_model = exp_config_data['retrieval_model']
    aws_region = exp_config_data['aws_region']
    retrieval_model_input_price = df[
        (df["model"] == retrieval_model) & (df["Region"] == exp_config_data['aws_region'])
        ]["input_price"]

    retrieval_model_output_price = df[
        (df["model"] == retrieval_model) & (df["Region"] == aws_region)
        ]["output_price"]

    retrieval_model_input_price = float(retrieval_model_input_price.values[0])  # Price per million tokens
    retrieval_model_output_price = float(retrieval_model_output_price.values[0])  # Price per million tokens

    retrieval_model_input_actual_cost = (retrieval_model_input_price * float(input_tokens)) / MILLION
    retrieval_model_output_actual_cost = (retrieval_model_output_price * float(output_tokens)) / MILLION
    return {'inference_input_cost': retrieval_model_input_actual_cost,
            'inference_output_cost': retrieval_model_output_actual_cost
            }


def calculate_sagemaker_inference_cost(inference_time):
    sagemaker_inference_cost = sagemaker_cost(inference_time, number_of_instances=1)
    return {'sagemaker_inference_cost': sagemaker_inference_cost}


def calculate_reranking_cost(exp_config_data, question_details):
    rerank_model_id = exp_config_data.get('rerank_model_id', "none")
    reranking_cost = 0
    if rerank_model_id and rerank_model_id != "none":
        reranker_model_price = df[(df["model"] == rerank_model_id) & (df["Region"] == aws_region)]["input_price"]
        if reranker_model_price.empty:
            logger.error(f"No reranker model {rerank_model_id} price found.")
            return 0
        reranker_model_price = float(reranker_model_price.values[0])  # Price per 1000 queries
        reranking_cost = (reranker_model_price * float(question_details['reranker_queries'])) / THOUSAND
    return {'reranking_cost': reranking_cost}



def sagemaker_cost(time, number_of_instances=1):
    instance_cost_per_hour = 1.210  # per hour ml.g5.2xlarge per model
    overall_cost = instance_cost_per_hour * number_of_instances * ((time / SECONDS_IN_MINUTE) / MINUTES_IN_HOUR)

    return overall_cost


def calculate_total_cost(exp_config_data, input_data):
    total_cost = 0
    question_details = calculate_experiment_question_details(input_data)
    for each_sample in input_data:
        try:
            inference_time = each_sample.get("answer_metadata", 0).get("latencyMs", 0)
            if exp_config_data['retrieval_service'] == "sagemaker":
                sagemaker_inference_cost = sagemaker_cost(inference_time, number_of_instances=1)
                each_sample['sagemaker_cost'] = {'sagemaker_inference_cost': sagemaker_inference_cost}
                total_cost += sagemaker_inference_cost
            else:
                inference_cost_dict = calculate_bedrock_inference_cost(each_sample, exp_config_data)
                each_sample['inference_cost'] = inference_cost_dict
                total_cost += inference_cost_dict['inference_input_cost']
                total_cost += inference_cost_dict['inference_output_cost']
            reranker_cost = calculate_reranking_cost(each_sample, question_details).get('reranking_cost', 0)
        except:
            logger.error(f"Error in calculating cost for sample {each_sample}")
            continue
        total_cost += reranker_cost
    return total_cost, input_data