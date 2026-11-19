"""Run this branch's nose-style setup methods under pytest."""

import pytest


def _defines(cls, name):
    return any(name in base.__dict__ for base in cls.__mro__)


@pytest.fixture(scope="class", autouse=True)
def _nose_class_setup(request):
    cls = request.cls
    if cls is not None and _defines(cls, "setUpAll"):
        cls.setUpAll()
    yield
    if cls is not None and _defines(cls, "tearDownAll"):
        cls.tearDownAll()


@pytest.fixture(autouse=True)
def _nose_test_setup(request):
    instance = getattr(request, "instance", None)
    if instance is None:
        yield
        return
    if _defines(type(instance), "setup"):
        instance.setup()
    yield
    if _defines(type(instance), "teardown"):
        instance.teardown()
