from typing import Any, Dict, List, Optional
from flotorch_core.evaluator.mistal import create_prompt, _make_api_request, create_payload, parse_response, _load_system_prompt
# from flotorch_core.evaluator.base_evaluator import BaseEvaluator
# from flotorch_core.evaluator.evaluation_item import EvaluationItem
# from flotorch_core.evaluator.metrics.metrics_keys import MetricKey
# from flotorch_core.evaluator.metrics.ragas_metrics.ragas_metrics import RagasEvaluationMetrics


class CustomEvaluator():
    """
    Evaluator that uses RAGAS metrics to score RAG-based QA performance.
    """

    def __init__(self, evaluator_llm):
        self.evaluator_llm = evaluator_llm
        # self.embedding_llm = embedding_llm
        print(self.evaluator_llm)

    def evaluate(
            self,
            data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        # example to fetch metrics, use like this
        for each in data:
            # print('-----------')
            prompt = _load_system_prompt(each)
            # print(prompt)
            payload = create_payload(prompt, self.evaluator_llm)
            # print(payload)
            # import json
            # with open("payload.json", "w") as f:
            #     json.dump(payload, f, indent=4)
            # print("-----"*10)
            # print(payload)
            response = _make_api_request(payload)
            each['response'] = parse_response(response['choices'][0]['message']['content'])
        return data