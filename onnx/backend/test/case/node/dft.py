# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np  # type: ignore

import onnx
from ..base import Base
from . import expect


class DFT(Base):

    @staticmethod
    def export() -> None:
        node = onnx.helper.make_node(
            'DFT',
            inputs=['x'],
            outputs=['y'],
            axis=1
        )
        x = np.arange(0, 100).reshape(10, 10).astype(np.float32)
        y = np.fft.fft(x, axis=0)

        x = x.reshape(1, 10, 10, 1)
        y = np.stack((y.real, y.imag), axis=2).astype(np.float32).reshape(1, 10, 10, 2)
        expect(node, inputs=[x], outputs=[y],
               name='test_dft')

        node = onnx.helper.make_node(
            'DFT',
            inputs=['x'],
            outputs=['y'],
            axis=2
        )
        x = np.arange(0, 100).reshape(10, 10).astype(np.float32)
        y = np.fft.fft(x, axis=1)

        x = x.reshape(1, 10, 10, 1)
        y = np.stack((y.real, y.imag), axis=2).astype(np.float32).reshape(1, 10, 10, 2)
        expect(node, inputs=[x], outputs=[y],
               name='test_dft_axis')

        node = onnx.helper.make_node(
            'DFT',
            inputs=['x'],
            outputs=['y'],
            inverse=1,
            axis=1
        )
        x = np.arange(0, 100, dtype=np.complex64).reshape(10, 10,)
        y = np.fft.ifft(x, axis=0)

        x = np.stack((x.real, x.imag), axis=2).astype(np.float32).reshape(1, 10, 10, 2)
        y = np.stack((y.real, y.imag), axis=2).astype(np.float32).reshape(1, 10, 10, 2)
        expect(node, inputs=[x], outputs=[y],
               name='test_dft_inverse')
