/******************************************************************************
** Copyright (c) 2015-2018, Intel Corporation                                **
** All rights reserved.                                                      **
**                                                                           **
** Redistribution and use in source and binary forms, with or without        **
** modification, are permitted provided that the following conditions        **
** are met:                                                                  **
** 1. Redistributions of source code must retain the above copyright         **
**    notice, this list of conditions and the following disclaimer.          **
** 2. Redistributions in binary form must reproduce the above copyright      **
**    notice, this list of conditions and the following disclaimer in the    **
**    documentation and/or other materials provided with the distribution.   **
** 3. Neither the name of the copyright holder nor the names of its          **
**    contributors may be used to endorse or promote products derived        **
**    from this software without specific prior written permission.          **
**                                                                           **
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS       **
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT         **
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR     **
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT      **
** HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,    **
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED  **
** TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR    **
** PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF    **
** LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING      **
** NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS        **
** SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.              **
******************************************************************************/
/* Hans Pabst (Intel Corp.)
******************************************************************************/
#include <libxsmm_source.h>

/* must match definitions in headeronly.c */
#if !defined(ITYPE)
# define ITYPE double
#endif
#if !defined(OTYPE)
# define OTYPE ITYPE
#endif


LIBXSMM_EXTERN LIBXSMM_MMFUNCTION_TYPE2(ITYPE, OTYPE) mmdispatch(int m, int n, int k);
LIBXSMM_EXTERN LIBXSMM_MMFUNCTION_TYPE2(ITYPE, OTYPE) mmdispatch(int m, int n, int k)
{
  LIBXSMM_MMFUNCTION_TYPE2(ITYPE, OTYPE) result;
#if defined(__cplusplus) /* C++ by chance: test libxsmm_mmfunction<> wrapper */
  const libxsmm_mmfunction<ITYPE, OTYPE> mmfunction(m, n, k);
  result = mmfunction.kernel().LIBXSMM_TPREFIX2(ITYPE, OTYPE, mm);
#else
  result = LIBXSMM_MMDISPATCH_SYMBOL2(ITYPE, OTYPE)(m, n, k,
    NULL/*lda*/, NULL/*ldb*/, NULL/*ldc*/,
    NULL/*alpha*/, NULL/*beta*/,
    NULL/*flags*/, NULL/*prefetch*/);
#endif
  return result;
}

