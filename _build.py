from setuptools.command.build_py import build_py as _build_py
import pathlib
from setuptools import Extension


class build_py(_build_py):
    def initialize_options(self):
        if self.distribution.ext_modules is None:
            return super().initialize_options()

        _ext_modules = []
        _magic_files = set()
        for m in self.distribution.ext_modules:
            _pysources = []
            _dirsources = []
            for s in m.sources:
                s = pathlib.Path(s)
                (_pysources if s.suffix == '.py' else _dirsources).append(s)
            m.sources = _pysources

            for s in _dirsources:
                for p in s.rglob("*.py"):
                    rp = p.relative_to(s)
                    if p.stem in ["__init__", "__main__"]:
                        _magic_files.add(str(p.parent))
                        continue

                    _ext_modules.append(
                        Extension(m.name + "." + str(rp.with_suffix("")), [str(p)])
                    )

        self.distribution.ext_modules.extend(_ext_modules)
        if self.distribution.packages is None:
            self.distribution.packages = []
        self.distribution.packages.extend(_magic_files)

        return super().initialize_options()

    def build_packages(self):
        for package in self.packages:
            package_dir = self.get_package_dir(package)
            modules = self.find_package_modules(package, package_dir)

            for package_, module, module_file in modules:
                if module_file.split("/")[-1] in ["__init__.py", "__main__.py"]:
                    assert package == package_
                    self.build_module(module, module_file, package)
