\
import json
from conan import Workspace
from conan import ConanFile
from conan.tools.files import save
from conan.tools.cmake import CMakeDeps, CMakeToolchain, cmake_layout


class MyWs(ConanFile):
    """ This is a special conanfile, used only for workspace definition of layout
    and generators. It shouldn't have requirements, tool_requirements. It shouldn't have
    build() or package() methods
    """
    settings = "os", "compiler", "build_type", "arch"

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def layout(self):
        cmake_layout(self)


class Ws(Workspace):
    def root_conanfile(self):
        return MyWs

    def build_order(self, order):
        super().build_order(order)  # default behavior prints the build order
        pkglist = " ".join([f'{it["ref"].name}:{it["folder"]}' for level in order for it in level])
        save(self, "build/conanws_build_order.cmake", f"set(CONAN_WS_BUILD_ORDER {pkglist})")
