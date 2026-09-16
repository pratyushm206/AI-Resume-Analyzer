from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError


LLM_TIMEOUT_SECONDS = 45


class LLMTimeoutError(TimeoutError):
    pass


class LLMProviderError(RuntimeError):
    pass


def run_with_timeout(func, *, timeout_seconds: int = LLM_TIMEOUT_SECONDS):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func)
        try:
            return future.result(timeout=timeout_seconds)
        except TimeoutError as exc:
            raise LLMTimeoutError(
                f"AI request timed out after {timeout_seconds} seconds."
            ) from exc
        except Exception as exc:
            message = str(exc)
            lower_message = message.lower()
            if (
                "503" in message
                or "unavailable" in lower_message
                or "high demand" in lower_message
                or "overloaded" in lower_message
            ):
                raise LLMProviderError(
                    "The AI model is currently experiencing high demand. Please try again in a few minutes."
                ) from exc
            raise LLMProviderError(
                "The AI request could not be completed right now. Please try again."
            ) from exc
