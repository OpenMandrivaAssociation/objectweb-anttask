Summary:	ObjectWeb Ant task
Name:		objectweb-anttask
Version:	1.3.2
Release:	8
Group:		Development/Java
License:	LGPLv2
Url:		http://forge.objectweb.org/projects/monolog/
Source0:	http://download.fr2.forge.objectweb.org/monolog/ow_util_ant_tasks_%{version}.tar.bz2
Patch0:	objectweb-anttask-1.3.2-filesets.patch
BuildArch:	noarch
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:	ant
BuildRequires:	java-rpmbuild
BuildRequires:	xalan-j2
Provides:	owanttask = %{epoch}:%{version}-%{release}

%description
ObjectWeb Ant task

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -c -q -n %{name}
%apply_patches
%remove_java_binaries

%build
export CLASSPATH=$(build-classpath xalan-j2 asm2/ )
export OPT_JAR_LIST=:
export JAVA_HOME=%{_prefix}/lib/jvm/java-1.6.0
ant jar jdoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}

install -m 644 output/lib/ow_util_ant_tasks.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir}
  ln -sf %{name}-%{version}.jar %{name}.jar
popd

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a output/jdoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

