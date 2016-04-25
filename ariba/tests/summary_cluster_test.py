import unittest
import copy
import filecmp
import os
from ariba import flag, summary_cluster

modules_dir = os.path.dirname(os.path.abspath(summary_cluster.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data')

class TestSummaryCluster(unittest.TestCase):
    def test_line2dict(self):
        '''Test _line2dict'''
        line = 'refname\treftype\t19\t78\tcluster\t120\t120\t98.33\tctg_name\t279\t24.4\t1\tSNP\tn\tA14T\t1\tA14T\tSNP\t13\t13\tA\t84\t84\tT\t17\t.\t17\tnoncoding1_n_A14T_N_ref has wild type, foo bar\tsome free text'

        expected = {
            'ref_name': 'refname',
            'ref_type': 'reftype',
            'flag': flag.Flag(19),
            'reads': 78,
            'cluster': 'cluster',
            'ref_len': 120,
            'ref_base_assembled': 120,
            'pc_ident': 98.33,
            'ctg': 'ctg_name',
            'ctg_len': 279,
            'ctg_cov': '24.4',
            'known_var': '1',
            'var_type': 'SNP',
            'var_seq_type': 'n',
            'known_var_change': 'A14T',
            'has_known_var': '1',
            'ref_ctg_change': 'A14T',
            'ref_ctg_effect': 'SNP',
            'ref_start': 13,
            'ref_end': 13,
            'ref_nt': 'A',
            'ctg_start': 84,
            'ctg_end': 84,
            'ctg_nt': 'T',
            'smtls_total_depth': '17',
            'smtls_alt_nt': '.',
            'smtls_alt_depth': '17',
            'var_description': 'noncoding1_n_A14T_N_ref has wild type, foo bar',
            'free_text': 'some free text'
        }

        self.assertEqual(summary_cluster.SummaryCluster.line2dict(line), expected)


    def test_add_data_dict(self):
        '''Test add_data_dict'''
        cluster = summary_cluster.SummaryCluster()
        self.assertTrue(cluster.name is None)
        line1 = 'refname\treftype\t19\t78\tcluster\t120\t120\t98.33\tctg_name\t279\t24.4\t1\tSNP\tn\tA14T\t1\tA14T\tSNP\t13\t13\tA\t84\t84\tT\t17\t.\t17\tnoncoding1_n_A14T_N_ref has wild type, foo bar\tsome free text'
        line2 = 'refname\treftype\t19\t78\tcluster2\t120\t120\t98.33\tctg_name\t279\t24.4\t1\tSNP\tn\tA14T\t1\tA14T\tSNP\t13\t13\tA\t84\t84\tT\t17\t.\t17\tnoncoding1_n_A14T_N_ref has wild type, foo bar\tsome free text'
        line3 = 'refname2\treftype\t19\t78\tcluster\t120\t120\t98.33\tctg_name\t279\t24.4\t1\tSNP\tn\tA14T\t1\tA14T\tSNP\t13\t13\tA\t84\t84\tT\t17\t.\t17\tnoncoding1_n_A14T_N_ref has wild type, foo bar\tsome free text'
        data_dict1 = summary_cluster.SummaryCluster.line2dict(line1)
        data_dict2 = summary_cluster.SummaryCluster.line2dict(line2)
        data_dict3 = summary_cluster.SummaryCluster.line2dict(line3)
        cluster.add_data_dict(data_dict1)
        self.assertEqual(cluster.name, data_dict1['cluster'])
        self.assertEqual(cluster.data,[data_dict1])
        with self.assertRaises(summary_cluster.Error):
            cluster.add_data_dict(data_dict2)

        with self.assertRaises(summary_cluster.Error):
            cluster.add_data_dict(data_dict3)

