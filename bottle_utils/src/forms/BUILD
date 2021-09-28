load("@pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "forms_lib",
    srcs = [] + glob(["*.py"]),
    data = [],
    visibility = [
        "//:__subpackages__",
    ],
    deps = [
        "//:tokens",
        requirement("WTForms"),
    ],
)
