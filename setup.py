#! /usr/bin/env python3

import distutils.cmd
import distutils.log
import os
import platform
import re
import subprocess
import sys
from distutils.version import LooseVersion
from os import listdir
from os.path import isfile, join
from shutil import copyfile, copymode, rmtree

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext


class AngularBuild(distutils.cmd.Command):
    description = 'run Pylint on Python source files'

    def initialize_options(self):
        return

    def finalize_options(self):
        return

    sub_commands = []
    user_options = []

    def run(self):
        build_site = True  # todo: temp
        if build_site:
            # SITE BUILD
            subprocess.check_call('git pull', cwd='lib/site', shell=True)
            subprocess.check_call('npm install', cwd='lib/site', shell=True)
            subprocess.check_call('npm run ng build -- --prod --base-href ./', cwd='lib/site', shell=True)

            mypath = 'lib/site/dist/zprsite/'
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

            if os.path.exists('src/distribution/static/'):
                rmtree('src/distribution/static/')
                os.makedirs('src/distribution/static/')

            # if os.path.exists('src/distribution/templates/'):
            #     rmtree('src/distribution/templates/')
            #     os.makedirs('src/distribution/templates/')

            # for f in filter(lambda x: x != 'index.html', onlyfiles):
            #     copyfile(mypath + f, 'src/distribution/static/' + f)

            for f in onlyfiles:
                copyfile(mypath + f, 'src/distribution/static/' + f)

            # copyfile(mypath + 'index.html', 'src/distribution/templates/' + 'index.html')

            # copy files and change path
            #


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)',
                                                   out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):

        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2 ** 32:
                cmake_args += ['-A', 'x64']
        else:
            cmake_args += ['-GUnix Makefiles']
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''), self.distribution.get_version())

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args,
                              cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=self.build_temp)

        # Copy *_test file to tests directory
        test_filename = 'distribution_test'

        if platform.system() == "Windows":
            test_filename = ''.join([test_filename, '.exe'])
            test_bin = os.path.join(self.build_temp, cfg, test_filename)
        else:
            test_bin = os.path.join(self.build_temp, test_filename)

        self.copy_test_file(test_bin)
        print()  # Add an empty line for cleaner output

    def copy_test_file(self, src_file):
        '''
        Copy ``src_file`` to ``dest_file`` ensuring parent directory exists.
        By default, message like `creating directory /path/to/package` and
        `copying directory /src/path/to/package -> path/to/package` are displayed on standard output. Adapted from scikit-build.
        '''
        # Create directory if needed
        dest_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'tests', 'bin')
        if dest_dir != "" and not os.path.exists(dest_dir):
            print("creating directory {}".format(dest_dir))
            os.makedirs(dest_dir)

        # Copy file
        dest_file = os.path.join(dest_dir, os.path.basename(src_file))
        print("copying {} -> {}".format(src_file, dest_file))
        copyfile(src_file, dest_file)
        copymode(src_file, dest_file)


setup(
    name='distribution',
    version='0.0.1',
    author='',
    author_email='',
    description='',
    long_description='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    ext_modules=[CMakeExtension('distribution/distribution')],
    cmdclass={'build_ext': CMakeBuild, 'site': AngularBuild},
    test_suite='tests',
    zip_safe=False,
    include_package_data=True,
)
