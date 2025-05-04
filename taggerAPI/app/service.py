from transformers import pipeline
from models import TagRequest, TagResponse, TagProbability
import logging
from fastapi import HTTPException
import constants

ZERO_SHOT_TASK = "zero-shot-classification"
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"

logger = logging.getLogger("uvicorn.error") 


class ZeroShotClassifierService:

    def __init__(self):
            
            try:
                from transformers import pipeline

                self.model = pipeline(ZERO_SHOT_TASK, model=ZERO_SHOT_MODEL)
                logger.info(constants.MODEL_OK)

            except Exception as e:

                logger.error(constants.MODEL_INIT_ERROR,e)
                raise RuntimeError(constants.MODEL_KO)

    def tag_message(self, request: TagRequest) -> TagResponse:

        if not request.text or not request.text.strip():
            logger.warning(constants.MESSAGE_EMPTY)
            raise HTTPException(status_code=422, detail=constants.MESSAGE_EMPTY_FAILURE)

        if not request.labels or not isinstance(request.labels, list) or len(request.labels) == 0:
            logger.warning(constants.TAG_INPUT_ERROR)
            raise HTTPException(status_code=422, detail=constants.TAG_INPUT_ERROR_MESSAGE)
        logger.info(constants.PROCESSING)

        try:
            result = self.model(request.text, request.labels)

        except Exception as e:
            logger.error(constants.INFERENCE_ERROR,e)
            raise HTTPException(
            status_code=500,
            detail=constants.INFERENCE_ERROR_MESSAGE,
            )
        
        threshold = max(0.3, 1 / len(request.labels))

        predicted_labels = [label for label, score in zip(result['labels'], result['scores']) if score >= threshold]


        probabilities = [
            TagProbability(label=label, score=float(score))
            for label, score in zip(result['labels'], result['scores'])
        ]

        if len(predicted_labels) == 0:

            logger.info(constants.TAGS_EMPTY)
            raise HTTPException(status_code=204, detail=constants.TAGS_EMPTY)

        return TagResponse(predicted_labels=predicted_labels, probabilities=probabilities)