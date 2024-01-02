---
description: >-
  How to setup airflow for local development, errors you might face and how to
  work around them?
---

# Setting Up Apache Airflow For Local Development in Mac M1

As I always say [start with the documentation](https://github.com/bhavaniravi/airflow/blob/main/CONTRIBUTING.rst). This documentation is all over the place, and you have to make a few decisions. Like whether to use breeze or virtualenv etc.,

My goto setup is to use the plain old virtualenv

### Fork and Clone the repo

```
git clone <forked-repo-url>
cd airflow
git remote add upstream git@github.com:apache/airflow.git
```

#### Install Mysql

```
brew install mysql
brew services start mysql
```

### Create Virtualenv

```
virtualenv -p python3 venv
```

### Activate Virtualenv

```
source venv/bin/activate
```

### Install required packages

```
pip install --upgrade -e ".[devel,google,postgres]"
```

I installed those 3 because I work with them predominantly. Every time I setup the project, I get an some error or the other

#### Some Red stuff you might receive

```
ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies
```

<pre><code><strong>ERROR: Command errored out with exit status 1:
</strong>   command: /Users/bhavaniravi/projects/airflow/venv/bin/python -u -c 'import io, os, sys, setuptools, tokenize; sys.argv[0] = '"'"'/private/var/folders/f6/d24p66nx1rj669t5dbk6gg780000gn/T/pip-install-lc77g8re/pygraphviz_80c4808c56e0490cb23cf6b35d596a18/setup.py'"'"'; __file__='"'"'/private/var/folders/f6/d24p66nx1rj669t5dbk6gg780000gn/T/pip-install-lc77g8re/pygraphviz_80c4808c56e0490cb23cf6b35d596a18/setup.py'"'"';f = getattr(tokenize, '"'"'open'"'"', open)(__file__) if os.path.exists(__file__) else io.StringIO('"'"'from setuptools import setup; setup()'"'"');code = f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' bdist_wheel -d /private/var/folders/f6/d24p66nx1rj669t5dbk6gg780000gn/T/pip-wheel-j8ki0jyn
       cwd: /private/var/folders/f6/d24p66nx1rj669t5dbk6gg780000gn/T/pip-install-lc77g8re/pygraphviz_80c4808c56e0490cb23cf6b35d596a18/
  Complete output (73 lines):
  running bdist_wheel
  running build
  running build_py
  creating build
  creating build/lib.macosx-10.14-arm64-3.8
  creating build/lib.macosx-10.14-arm64-3.8/pygraphviz
  copying pygraphviz/scraper.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz
  copying pygraphviz/graphviz.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz
  copying pygraphviz/__init__.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz
  copying pygraphviz/agraph.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz
  copying pygraphviz/testing.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz
  creating build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_unicode.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_scraper.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_readwrite.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_string.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/__init__.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_html.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_node_attributes.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_drawing.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_repr_mimebundle.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_subgraph.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_close.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_edge_attributes.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_clear.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_layout.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_attribute_defaults.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  copying pygraphviz/tests/test_graph.py -> build/lib.macosx-10.14-arm64-3.8/pygraphviz/tests
  running egg_info
  writing pygraphviz.egg-info/PKG-INFO
  writing dependency_links to pygraphviz.egg-info/dependency_links.txt
  writing top-level names to pygraphviz.egg-info/top_level.txt
  reading manifest file 'pygraphviz.egg-info/SOURCES.txt'
  reading manifest template 'MANIFEST.in'
  warning: no files found matching '*.png' under directory 'doc'
  warning: no files found matching '*.txt' under directory 'doc'
  warning: no files found matching '*.css' under directory 'doc'
  warning: no previously-included files matching '*~' found anywhere in distribution
  warning: no previously-included files matching '*.pyc' found anywhere in distribution
  warning: no previously-included files matching '.svn' found anywhere in distribution
  no previously-included directories found matching 'doc/build'
  adding license file 'LICENSE'
  writing manifest file 'pygraphviz.egg-info/SOURCES.txt'
  copying pygraphviz/graphviz.i -> build/lib.macosx-10.14-arm64-3.8/pygraphviz
  copying pygraphviz/graphviz_wrap.c -> build/lib.macosx-10.14-arm64-3.8/pygraphviz
  running build_ext
  building 'pygraphviz._graphviz' extension
  creating build/temp.macosx-10.14-arm64-3.8
  creating build/temp.macosx-10.14-arm64-3.8/pygraphviz
  clang -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -iwithsysroot/System/Library/Frameworks/System.framework/PrivateHeaders -iwithsysroot/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.8/Headers -arch arm64 -arch x86_64 -Werror=implicit-function-declaration -DSWIG_PYTHON_STRICT_BYTE_CHAR -I/Users/bhavaniravi/projects/airflow/venv/include -I/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/include/python3.8 -c pygraphviz/graphviz_wrap.c -o build/temp.macosx-10.14-arm64-3.8/pygraphviz/graphviz_wrap.o
  pygraphviz/graphviz_wrap.c:1756:7: warning: 'tp_print' is deprecated [-Wdeprecated-declarations]
        0,                                    /* tp_print */
        ^
  /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/include/python3.8/cpython/object.h:260:5: note: 'tp_print' has been explicitly marked deprecated here
      Py_DEPRECATED(3.8) int (*tp_print)(PyObject *, FILE *, int);
      ^
  /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/include/python3.8/pyport.h:515:54: note: expanded from macro 'Py_DEPRECATED'
  #define Py_DEPRECATED(VERSION_UNUSED) __attribute__((__deprecated__))
                                                       ^
  pygraphviz/graphviz_wrap.c:1923:7: warning: 'tp_print' is deprecated [-Wdeprecated-declarations]
        0,                                    /* tp_print */
        ^
  /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/include/python3.8/cpython/object.h:260:5: note: 'tp_print' has been explicitly marked deprecated here
      Py_DEPRECATED(3.8) int (*tp_print)(PyObject *, FILE *, int);
      ^
  /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/include/python3.8/pyport.h:515:54: note: expanded from macro 'Py_DEPRECATED'
  #define Py_DEPRECATED(VERSION_UNUSED) __attribute__((__deprecated__))
                                                       ^
  pygraphviz/graphviz_wrap.c:2711:10: fatal error: 'graphviz/cgraph.h' file not found
  #include "graphviz/cgraph.h"
           ^~~~~~~~~~~~~~~~~~~
  2 warnings and 1 error generated.
  error: command 'clang' failed with exit status 1
  ----------------------------------------
  ERROR: Failed building wheel for pygraphviz
</code></pre>

To mitigate this error

```
brew install graphviz
brew info graphviz
```

You will get an installation path. Add that to this env variable

```
export GRPAHVIZ_DIR=/opt/homebrew/Cellar/graphviz/2.48.0
```

### Pre-commit

```
pre-commit install
```

### Running Mypy

```
mypy <filepath>
```

### Running Pytest

```
pytest <path-to-file>::function_name
pytest <path-to-file>::className::func_name
```

***

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
