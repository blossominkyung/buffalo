# -*- coding: utf-8 -*-
import os
import unittest
from buffalo.algo.als import ALS
from buffalo.algo.options import AlsOption
from buffalo.misc.log import set_log_level, get_log_level
from buffalo.data.mm import MatrixMarketOptions

from .base import TestBase


class TestALS(TestBase):
    def test0_get_default_option(self):
        AlsOption().get_default_option()
        self.assertTrue(True)

    def test1_is_valid_option(self):
        opt = AlsOption().get_default_option()
        self.assertTrue(AlsOption().is_valid_option(opt))
        opt['save_best_only'] = 1
        self.assertRaises(RuntimeError, AlsOption().is_valid_option, opt)
        opt['save_best_only'] = False
        self.assertTrue(AlsOption().is_valid_option(opt))

    def test2_init_with_dict(self):
        opt = AlsOption().get_default_option()
        ALS(opt)
        self.assertTrue(True)

    def test3_init(self):
        set_log_level(3)
        opt = AlsOption().get_default_option()
        data_opt = MatrixMarketOptions().get_default_option()
        data_opt.input.main = self.mm_path
        data_opt.input.uid = self.uid_path
        data_opt.input.iid = self.iid_path

        als = ALS(opt, data_opt=data_opt)
        self.assertTrue(True)
        self.temp_files.append(data_opt.data.path)
        als.init_factors()
        self.assertTrue(als.P.shape, (5, 20))
        self.assertTrue(als.Q.shape, (3, 20))

    def test4_train(self):
        set_log_level(3)
        opt = AlsOption().get_default_option()
        opt.d = 5

        data_opt = MatrixMarketOptions().get_default_option()
        data_opt.input.main = self.mm_path
        data_opt.input.uid = self.uid_path
        data_opt.input.iid = self.iid_path
        self.temp_files.append(data_opt.data.path)

        als = ALS(opt, data_opt=data_opt)
        als.init_factors()
        als.train()

    def test5_train_ml_20m(self):
        set_log_level(3)
        opt = AlsOption().get_default_option()
        opt.num_workers = 8

        data_opt = MatrixMarketOptions().get_default_option()
        data_opt.input.main = './ml-20m-mm/main'
        data_opt.input.uid = './ml-20m-mm/uid'
        data_opt.input.iid = './ml-20m-mm/iid'
        data_opt.data.path = './ml20.h5py'
        data_opt.data.use_cache = True

        als = ALS(opt, data_opt=data_opt)
        als.init_factors()
        als.train()


if __name__ == '__main__':
    unittest.main()