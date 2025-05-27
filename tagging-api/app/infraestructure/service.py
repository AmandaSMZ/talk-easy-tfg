
import logging
from typing import List
from fastapi import HTTPException
from app import constants
from app.api.schemas import TagOut
from app.infraestructure.db.repository import get_tag_ids_by_names

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
                logger.error(f"{constants.MODEL_INIT_ERROR}: {e}")
                raise RuntimeError(constants.MODEL_KO)

    def tag_message(self, request: str, tags):

        if not request or not request.strip():
            logger.warning(constants.MESSAGE_EMPTY)
            raise HTTPException(status_code=422, detail=constants.MESSAGE_EMPTY_FAILURE)

        if not tags or not isinstance(tags, list) or len(tags) == 0:
            logger.warning(constants.TAG_INPUT_ERROR)
            raise HTTPException(status_code=422, detail=constants.TAG_INPUT_ERROR_MESSAGE)
        
        logger.info(constants.PROCESSING)

        try:
            result = self.model(request, tags)

        except Exception as e:
            logger.error(f"{constants.INFERENCE_ERROR}: {e}")
            raise HTTPException(
            status_code=500,
            detail=constants.INFERENCE_ERROR_MESSAGE,
            )
        
        threshold = max(0.5, 1 / len(request.labels))

        predicted_labels = [str(label) for label, score in zip(result['labels'], result['scores']) if score >= threshold]

        if len(predicted_labels) == 0:
            logger.info(constants.TAGS_EMPTY)
            raise HTTPException(status_code=204, detail=constants.TAGS_EMPTY)
        
        labels_id = get_tag_ids_by_names(predicted_labels)

        return [TagOut(id=label) for label in labels_id]

classifier_service = ZeroShotClassifierService()