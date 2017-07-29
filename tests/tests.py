import unittest
import firefox_session_merger as merger

class FirefoxSessionMergerTestSuite(unittest.TestCase):

    def test_file_load(self):
        session = merger.load_sessionstore_file("tests/testcase1.json")
        self.assertEqual(len(session.get("windows")), 1)

    def test_multiple_file_load(self):
        sessions = list(merger.load_sessionstore_files(["tests/testcase1.json", "tests/testcase2.json"]))
        self.assertEqual(len(sessions), 2)
    
    def test_extract_all_tabs(self):
        session = merger.load_sessionstore_file("tests/testcase1.json")
        tabs = list(merger.extract_all_tabs(session))
        self.assertEqual(len(tabs), 2)
        for tab in tabs:
            entries = tab.get("entries")
            self.assertEqual(len(entries), 1)
            self.assertTrue(entries[0].get("url").startswith("about:"))

    def test_flatten_session(self):
        session = merger.load_sessionstore_file("tests/testcase_flatten.json")
        merger.flatten_session(session)
        self.assertEqual(len(session.get("windows")), 1)
        tabs = list(session.get("windows")[0].get("tabs"))
        self.assertEqual(len(tabs), 2)
    
    def test_urls_from_session(self):
        session = merger.load_sessionstore_file("tests/testcase1.json")
        urls = list(merger.urls_from_session(session))
        self.assertEqual(len(urls), 2)
        self.assertTrue(urls[0],"about:startpage")
        self.assertTrue(urls[1],"about:preferences")
    
    def test_has_duplicate_in_session(self):
        session = merger.load_sessionstore_file("tests/testcase1.json")
        other_session = merger.load_sessionstore_file("tests/testcase2.json")
        session_tabs = list(merger.extract_all_tabs(session))
        other_session_tabs = list(merger.extract_all_tabs(other_session))
        #testing agains tabs taken from the same session
        self.assertTrue(merger.has_duplicate_in_session(session,session_tabs[0]))
        self.assertTrue(merger.has_duplicate_in_session(session,session_tabs[1]))
        #testing agains tabs taken from the different session
        self.assertTrue(merger.has_duplicate_in_session(session,other_session_tabs[0]))
        self.assertFalse(merger.has_duplicate_in_session(session,other_session_tabs[1]))
    
    def test_simple_merge_into(self):
        sessions = list(merger.load_sessionstore_files(["tests/testcase1.json", "tests/testcase2.json"]))
        merger.simple_merge_into(sessions[0], sessions[1])
        main_session = sessions[0]
        self.assertEqual(len(main_session.get("windows")), 2)
    
    def test_deep_merge_into(self):
        sessions = list(merger.load_sessionstore_files(["tests/testcase1.json", "tests/testcase2.json"]))
        merger.deep_merge_into(sessions[0], sessions[1])
        main_session = sessions[0]
        self.assertEqual(len(main_session.get("windows")), 1)
        urls = list(merger.urls_from_session(main_session))
        self.assertEqual(len(urls), 3)
        self.assertTrue(urls[0],"about:startpage")
        self.assertTrue(urls[1],"about:preferences")
        self.assertTrue(urls[2],"about:addons")

if __name__ == '__main__':
    unittest.main() 
