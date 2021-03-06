#!/usr/bin/env python
###############################################################################
# Copyright (c) 2014-2018, Intel Corporation                                  #
# All rights reserved.                                                        #
#                                                                             #
# Redistribution and use in source and binary forms, with or without          #
# modification, are permitted provided that the following conditions          #
# are met:                                                                    #
# 1. Redistributions of source code must retain the above copyright           #
#    notice, this list of conditions and the following disclaimer.            #
# 2. Redistributions in binary form must reproduce the above copyright        #
#    notice, this list of conditions and the following disclaimer in the      #
#    documentation and/or other materials provided with the distribution.     #
# 3. Neither the name of the copyright holder nor the names of its            #
#    contributors may be used to endorse or promote products derived          #
#    from this software without specific prior written permission.            #
#                                                                             #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS         #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT           #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR       #
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT        #
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,      #
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED    #
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR      #
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF      #
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING        #
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS          #
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                #
###############################################################################
# Hans Pabst (Intel Corp.)
###############################################################################
import libxsmm_utilities
import sys
import os


if __name__ == "__main__":
    argc = len(sys.argv)
    if (1 < argc):
        arg1_filename = [sys.argv[1], ""]["0" == sys.argv[1]]
        arg1_isfile = os.path.isfile(arg1_filename)
        base = 1
        if (arg1_isfile):
            print("#if !defined(_WIN32)")
            print("{ static const char *const build_state =")
            print("#   include \"" + sys.argv[1] + "\"")
            print("  ;")
            print("  internal_build_state = build_state;")
            print("}")
            print("#endif")
            base = 2
        if ((base + 2) < argc):
            precision = int(sys.argv[base+0])
            threshold = int(sys.argv[base+1])
            mnklist = libxsmm_utilities.load_mnklist(sys.argv[base+2:], 0)
            print("/* omit registering code if JIT is enabled"
                  " and if an ISA extension is found")
            print(" * which is beyond the static code"
                  " path used to compile the library")
            print(" */")
            print("#if (0 != LIBXSMM_JIT) && !defined(__MIC__)")
            print("/* check if target arch. permits execution"
                  " (arch. may be overridden) */")
            print("if (LIBXSMM_STATIC_TARGET_ARCH"
                  " <= libxsmm_target_archid &&")
            print("   (LIBXSMM_X86_SSE3 > libxsmm_target_archid "
                  "/* JIT code gen. is not available */")
            print("    /* condition allows to avoid JIT "
                  "(if static code is good enough) */")
            print("    || LIBXSMM_STATIC_TARGET_ARCH"
                  " == libxsmm_target_archid))")
            print("#endif")
            print("{")
            print("  libxsmm_gemm_descriptor desc;")
            print("  libxsmm_xmmfunction func;")
            print("  unsigned int hash, indx;")
            print("# if defined(_MSC_VER)")
            print("#   pragma warning(push)")
            print("#   pragma warning(disable: 4127)")
            print("# endif")
            for mnk in mnklist:
                mstr, nstr, kstr, mnkstr = \
                    str(mnk[0]), str(mnk[1]), str(mnk[2]), \
                    "_".join(map(str, mnk))
                mnksig = mstr + ", " + nstr + ", " + kstr
                ldxsig = mstr + ", " + kstr + ", " + mstr
                # prefer registering double-precision kernels
                # when approaching an exhausted registry
                if (1 != precision):  # only double-precision
                    print("  if (LIBXSMM_GEMM_NO_BYPASS_DIMS(" + mnksig + ")" +
                          " && LIBXSMM_GEMM_NO_BYPASS_DIMS(" + ldxsig + ")) {")
                    print("    LIBXSMM_GEMM_DESCRIPTOR(desc, " +
                          "LIBXSMM_GEMM_PRECISION_F64, LIBXSMM_FLAGS,")
                    print("      " + mnksig + ", " + ldxsig + ", " +
                          "LIBXSMM_ALPHA, LIBXSMM_BETA, INTERNAL_PREFETCH);")
                    print("    hash = libxsmm_crc32(&desc, " +
                          "LIBXSMM_DESCRIPTOR_MAXSIZE, LIBXSMM_HASH_SEED);")
                    print("    indx = LIBXSMM_HASH_MOD(hash, " +
                          "LIBXSMM_CAPACITY_REGISTRY);")
                    print("    func.dmm = (libxsmm_dmmfunction)libxsmm_dmm_" +
                          mnkstr + ";")
                    print("    internal_register_static_code(" +
                          "&desc, indx, hash, func, new_registry);")
                    print("  }")
            for mnk in mnklist:
                mstr, nstr, kstr, mnkstr = \
                    str(mnk[0]), str(mnk[1]), str(mnk[2]), \
                    "_".join(map(str, mnk))
                mnksig = mstr + ", " + nstr + ", " + kstr
                ldxsig = mstr + ", " + kstr + ", " + mstr
                # prefer registering double-precision kernels
                # when approaching an exhausted registry
                if (2 != precision):  # only single-precision
                    print("  if (LIBXSMM_GEMM_NO_BYPASS_DIMS(" + mnksig + ")" +
                          " && LIBXSMM_GEMM_NO_BYPASS_DIMS(" + ldxsig + ")) {")
                    print("    LIBXSMM_GEMM_DESCRIPTOR(desc, " +
                          "LIBXSMM_GEMM_PRECISION_F32, LIBXSMM_FLAGS,")
                    print("      " + mnksig + ", " + ldxsig + ", " +
                          "LIBXSMM_ALPHA, LIBXSMM_BETA, INTERNAL_PREFETCH);")
                    print("    hash = libxsmm_crc32(&desc, " +
                          "LIBXSMM_DESCRIPTOR_MAXSIZE, LIBXSMM_HASH_SEED);")
                    print("    indx = LIBXSMM_HASH_MOD(hash, " +
                          "LIBXSMM_CAPACITY_REGISTRY);")
                    print("    func.smm = (libxsmm_smmfunction)libxsmm_smm_" +
                          mnkstr + ";")
                    print("    internal_register_static_code(" +
                          "&desc, indx, hash, func, new_registry);")
                    print("  }")
            print("# if defined(_MSC_VER)")
            print("#   pragma warning(pop)")
            print("# endif")
            print("}")
    else:
        sys.tracebacklimit = 0
        raise ValueError(sys.argv[0] + ": wrong number of arguments!")
