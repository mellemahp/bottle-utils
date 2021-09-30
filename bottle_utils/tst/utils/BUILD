load("@pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "testing_utils",
    srcs = [] + glob(["*.py"]),
    data = [],
    visibility = [
        "//:__subpackages__",
    ],
    deps = [
        requirement("redislite")
    ],
)