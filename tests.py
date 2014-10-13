"""
Test the Sprockets Command Line Interface

"""
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock

from sprockets import cli


class InitializationTests(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args')
    @mock.patch('pkg_resources.iter_entry_points')
    @mock.patch('importlib.import_module')
    def setUp(self, import_module, iter_entry_points, parse_args):
        self.import_module = import_module
        self.iter_entry_points = iter_entry_points
        self.parse_args = parse_args

        self.app_points = [mock.Mock(name='test_app',
                                     module_name='mock_app')]
        self.ctrl_points = [mock.Mock(name='test_http',
                                      module_name='mock_http')]
        self.loader_points = [mock.Mock(name='test_loader',
                                        module_name='mock_auto_loader')]

        self.mock_app = mock.Mock()
        self.mock_controller = mock.Mock()
        self.mock_controller.add_cli_arguments = self.add_cli_arguments = \
            mock.Mock()
        self.mock_auto_loader = mock.Mock()

        def entry_point_side_effect(*args, **kwargs):
            if kwargs.get('group') == 'sprockets.controller':
                return self.ctrl_points
            elif kwargs.get('group') == 'sprockets.auto-loader':
                return self.loader_points
            elif kwargs.get('group') == 'sprockets.test_http.app':
                return self.app_points
        self.iter_entry_points.side_effect = entry_point_side_effect

        def import_module_side_effect(*args, **kwargs):
            if args[0] == 'mock_app':
                return self.mock_app
            elif args[0] == 'mock_http':
                return self.mock_controller
            elif args[0] == 'mock_auto_loader':
                return self.mock_auto_loader
        self.import_module.side_effect = import_module_side_effect
        self.obj = cli.CLI()

    def test_pkg_resources_iterated(self):
        calls = [mock.call(group='sprockets.auto-loader'),
                 mock.call(group='sprockets.controller')]
        self.iter_entry_points.assert_has_calls(calls)

    def test_controller_packages_imported(self):
        self.import_module.assert_has_calls([mock.call('mock_auto_loader'),
                                             mock.call('mock_http')])

    #def test_controller_argparse_method_invoked(self):
    #    self.add_cli_arguments.assert_called_once_with(self.obj.arg_parser)
