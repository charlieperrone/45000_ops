import unittest
from unittest.mock import patch, mock_open
import os
import subprocess
import json
from create import clear_directory, create_silent_files, create_silent_stereo_file, main, open_file

class TestCreateScript(unittest.TestCase):

    @patch('create.os.path.exists')
    @patch('create.os.listdir')
    @patch('create.os.unlink')
    @patch('create.shutil.rmtree')
    @patch('create.os.path.join')
    def test_clear_directory(self, mock_join, mock_rmtree, mock_unlink, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['file1.wav', 'file2.wav']
        mock_join.side_effect = lambda *args: '/'.join(args)
        
        clear_directory('/fake/dir')
        
        # Debugging output
        print(f"Unlink calls: {mock_unlink.mock_calls}")
        print(f"Rmtree calls: {mock_rmtree.mock_calls}")
        
        mock_unlink.assert_any_call('/fake/dir/file1.wav')
        mock_unlink.assert_any_call('/fake/dir/file2.wav')

    @patch('create.subprocess.check_output')
    @patch('create.os.path.join')
    @patch('create.subprocess.run')
    def test_create_silent_files(self, mock_run, mock_join, mock_check_output):
        mock_check_output.return_value = b'10.0'
        mock_join.side_effect = lambda *args: '/'.join(args)
        
        create_silent_files('original.wav', '/output/dir', 3, 1)
        
        self.assertEqual(mock_run.call_count, 3)
        mock_run.assert_any_call(['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '10.0', '/output/dir/TRACK2.wav'], check=False)

    @patch('create.subprocess.check_output')
    @patch('create.os.path.join')
    @patch('create.subprocess.run')
    def test_create_silent_stereo_file(self, mock_run, mock_join, mock_check_output):
        mock_check_output.return_value = b'10.0'
        mock_join.side_effect = lambda *args: '/'.join(args)
        
        create_silent_stereo_file('original.wav', '/output/dir')
        
        mock_run.assert_called_once_with(['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-t', '10.0', '/output/dir/TRACKM.wav'], check=False)

    @patch('create.open_file', new_callable=mock_open)
    @patch('create.json.dump')
    @patch('create.subprocess.run')
    @patch('create.os.makedirs')
    @patch('create.os.path.isdir')
    @patch('create.os.listdir')
    @patch('create.clear_directory')
    @patch('create.subprocess.check_output')
    def test_main(self, mock_clear_directory, mock_listdir, mock_isdir, mock_makedirs, mock_run, mock_json_dump, mock_open, mock_check_output):
        mock_isdir.side_effect = lambda path: path == '/input/dir'
        mock_listdir.return_value = ['file1.wav']
        mock_check_output.return_value = b'10.0'
        
        main('/input/dir/file1.wav', '/output/dir', 'Test Song')
        
        mock_clear_directory.assert_called_once_with('/output/dir')
        mock_makedirs.assert_called_once_with('/output/dir', exist_ok=True)
        mock_run.assert_called_with(['ffmpeg', '-i', '/input/dir/file1.wav', '-ac', '1', '/output/dir/TRACK1.wav'], check=True)
        mock_json_dump.assert_called_once()
        self.assertTrue(mock_open.called)

if __name__ == '__main__':
    unittest.main()
