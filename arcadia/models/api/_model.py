import contextlib
from functools import lru_cache
import gc
from pathlib import Path
import shutil
from typing import ClassVar

import attrs
from transformers import pipeline


def release_gpu() -> None:
    gc.collect()
    with contextlib.suppress(ImportError):
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()


def clear_storage(model_id: str) -> None:
    from huggingface_hub.constants import HF_HOME

    owner, name = model_id.split("/", 1)
    cache_dir = Path(HF_HOME) / "hub" / f"models--{owner}--{name}"
    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)


@attrs.frozen
class Model:
    owner: ClassVar[str]
    _model: ClassVar[str]

    @property
    def model(self) -> str:
        return self._model

    def __str__(self) -> str:
        return self.model

    @property
    def id(self) -> str:
        return f"{self.owner}/{self.model}"

    @property
    def huggginface(self) -> str:
        return f"https://huggingface.co/{self.id}"

    @lru_cache(maxsize=None)
    def pipeline(self, task: str):
        return pipeline(task, model=self.id)

    def release(self) -> None:
        release_gpu()
        clear_storage(self.id)
