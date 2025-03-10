#
# This is template for pure python modules (noarch)
# use template-specs/python-ext.spec for binary python packages
#
#
# Conditional build:
%bcond_with	doc	# don't build doc
# Fails on aetypes
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

# NOTES:
# - 'module' should match the Python import path (first component?)
# - 'egg_name' should equal to Python egg name
# - 'pypi_name' must match the Python Package Index name
%define		module		pbkdf2
%define		egg_name	pbkdf2
%define		pypi_name	pbkdf2
Summary:	Python implementation of password-based key derivation function, PBKDF2
# Summary(pl.UTF-8):	-
Name:		python-%{pypi_name}
Version:	1.3
Release:	8
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/02/c0/6a2376ae81beb82eda645a091684c0b0becb86b972def7849ea9066e3d5e/pbkdf2-%{version}.tar.gz
# Source0-md5:	40cda566f61420490206597243dd869f
URL:		http://www.dlitz.net/software/python-pbkdf2/
#URL:		https://pypi.python.org/pypi/MODULE
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
# replace with other requires if defined in setup.py
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Module which implements the password-based key derivation function,
PBKDF2, specified in RSA PKCS#5 v2.0.

# %description -l pl.UTF-8

%package -n python3-%{pypi_name}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}

%description -n python3-%{pypi_name} -l pl.UTF-8

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Pythona %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.txt
%{py_sitescriptdir}/%{module}.pyo
%{py_sitescriptdir}/%{module}.pyc
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.txt
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/%{module}.*.pyc
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
