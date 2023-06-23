# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
######################## eval lenet example ########################
eval lenet according to model file:
python eval.py --data_path /YourDataPath --ckpt_path Your.ckpt
"""

import os
import ast
import argparse
import mindspore.nn as nn
from mindspore import context
from mindspore.train.serialization import load_checkpoint, load_param_into_net
from mindspore.train import Model
from mindspore.nn.metrics import Accuracy
from src.dataset import create_dataset
from src.config import mnist_cfg as cfg
from src.lenet import LeNet5

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MindSpore Lenet Example')
    # 设备设置
    parser.add_argument('--device_target', type=str, default="CPU", choices=['Ascend', 'GPU', 'CPU'],
                        help='device where the code will be implemented (default: Ascend)')
    parser.add_argument('--data_path', type=str, default="./MNIST_Data",
                        help='path where the dataset is saved')
    parser.add_argument('--ckpt_path', type=str, default="./ckpt/checkpoint_lenet-10_1875.ckpt", help='if mode is test, must provide\
                        path where the trained ckpt file')
    parser.add_argument('--dataset_sink_mode', type=ast.literal_eval,
                        default=False, help='dataset_sink_mode is False or True')

    args = parser.parse_args()

    context.set_context(mode=context.GRAPH_MODE, device_target=args.device_target)

    network = LeNet5(cfg.num_classes)
    #设定loss函数
    net_loss = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction="mean")
    repeat_size = cfg.epoch_size
    #设定优化器
    net_opt = nn.Momentum(network.trainable_params(), cfg.lr, cfg.momentum)
    #编译形成模型
    model = Model(network, net_loss, net_opt, metrics={"Accuracy": Accuracy()})
    print("============== Starting Testing ==============")
    param_dict = load_checkpoint(args.ckpt_path)
    load_param_into_net(network, param_dict)
    ds_eval = create_dataset(os.path.join(args.data_path, "test"),
                             cfg.batch_size,
                             1)
    acc = model.eval(ds_eval, dataset_sink_mode=args.dataset_sink_mode)
    print("============== {} ==============".format(acc))
