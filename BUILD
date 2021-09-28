load("@pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "bottle-utils",
    srcs = [] + glob(["utils/**/*.py"], exclude=["**/__pycache__/**"]),
    deps = [
        requirement("redis"),
        requirement("structlog"),
        requirement("bottle"),
        requirement("redislite"),
        requirement("peewee"),
        requirement("WTForms"),
        requirement("prometheus-client"),
        requirement("Jinja2")
    ],
    visibility = ["//visibility:public"]
)