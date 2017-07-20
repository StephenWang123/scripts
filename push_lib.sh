#!/bin/bash

VER="6.0.4"

# version info - 2 cases
if [ -f ./version.txt ]; then
    ver=`cat ./version.txt`
    # if more than one modules, take the version of RECON 
    multi=`echo $ver |grep -s RECON`
    if [ ! -z "$multi" ]; then
        ver=`echo $multi|cut -d'=' -f2|cut -d' ' -f1`
        echo "Info: Use the version of reconstruction code."
    fi

    # for 6.0.4 & up, use build dir to host insp libs
    if [ "${ver}1" -ge "${VER}1" ]; then
        files=`ls build/*.so` 
        num_file=`ls build/*.so|wc -l` 
    else
        files=`ls build/*/*/*.so` 
        num_file=`ls build/*/*/*.so |wc -l` 
    fi    
elif [ -f ./version ]; then
    source ./version
    ver=${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_LEVEL}
    files=`ls */*/librecon_*.so */*/libiq*.so` 
    num_file=`ls  */*/librecon_*.so */*/libiq*.so |wc -l` 
elif [ -f ./CMakeLists.txt ]; then
    ver=`grep -e SET CMakeLists.txt|grep -s -e INSP_VER|cut -d'"' -f2`
    num_file1=`ls build-release/lib/*.so |wc -l` 
else
    echo "Error: check version extracting code!"
    exit 1
fi
echo "The version is $ver."


#constant
OS_VERSION=`lsb_release -r -s`
PRODUCT=LIB

#construct lib dir
job=`echo ${JOB_NAME} |cut -d'_' -f1`
lib_dir=/net/eng-svnshare/svnshare/builds/collabnet/${PRODUCT}/${job}_${ver}-f${OS_VERSION}-${SVN_REVISION}/

#check lib_dir
if [ ! -d $lib_dir ] ; then
    mkdir -p $lib_dir
fi

#display messages
echo "OS of this build is fc$OS_VERSION"
echo "Subversion revision: $SVN_REVISION"

#copy *.so to share drive
if [ ${num_file} > 0 ]; then
    echo  "${num_file} lib file(s) of this build will be pushed into $lib_dir"
#    cp  build/*/*/*.so build/*.so build/*/*.so ${lib_dir}  
    cp  ${files} ${lib_dir}  
    echo "Done"
elif [ ${num_file1} > 0 ]; then
    echo  "${num_file1} lib file(s) of this build will be pushed into $lib_dir"
    cp  build-release/lib/*.so ${lib_dir}  
    echo "Done"
fi
