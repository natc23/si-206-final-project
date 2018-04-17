import unittest
import final_project as final
import sqlite3


#You must create at least 3 test cases and use at least 15 assertions or calls to ‘fail( )’.
#Your tests should show that you are able to access data from all of your sources,
#that your database is correctly constructed and can satisfy queries that are necessary for your program,
#and that your data processing produces the results and data structures you need for presentation.


class TestDataAccess(unittest.TestCase):

    def testAccountInfo(self):
        account_data = final.get_account_info('eddieredmaynelesmis.tumblr.com')
        self.assertEqual(account_data[0][0], 'eddieredmaynelesmis')
        self.assertEqual(account_data[0][4], 508)

    def testPostInfo(self):
        post_info = final.get_post_data('eddieredmaynelesmis.tumblr.com')
        self.assertEqual(post_info[0][3], 'photo')
        self.assertEqual(post_info[0][5], 60)

    def testPageScrape(self):
        scrape_data = final.get_best_tumblrs()
        self.assertEqual(scrape_data[0], 'adambellefeuil.tumblr.com')


class TestDatabase(unittest.TestCase):
    final.init_db()
    final.insert_data('eddieredmaynelesmis.tumblr.com')
    final.update_id_data()

    def testBlogDB(self):
        conn = sqlite3.connect(final.DBNAME)
        cur = conn.cursor()

        cur.execute('SELECT Username FROM Blogs WHERE Username = "eddieredmaynelesmis"')
        for row in cur:
            un = row[0]

        cur.execute('SELECT PostsCount FROM Blogs WHERE Username = "eddieredmaynelesmis"')
        for row in cur:
            pc = row[0]

        cur.execute('SELECT CanAsk FROM Blogs WHERE Username = "eddieredmaynelesmis"')
        for row in cur:
            ca = row[0]

        self.assertEqual(un, 'eddieredmaynelesmis')
        self.assertEqual(pc, 508)
        self.assertEqual(ca, 'yes')

        conn.close()

    def testPostsDB(self):
        conn = sqlite3.connect(final.DBNAME)
        cur = conn.cursor()

        cur.execute('SELECT COUNT(*) FROM Posts WHERE PostType = "photo"')
        for row in cur:
            pt_count = row[0]

        cur.execute('SELECT UserId FROM Posts WHERE BlogName = "eddieredmaynelesmis"')
        for row in cur:
            u_id = row[0]

        self.assertEqual(pt_count, 49)
        self.assertEqual(u_id, 1)

        conn.close()


class TestDataProcessing(unittest.TestCase):

    def testNotesData(self):
        x = final.GraphData()
        x.notes_data('eddieredmaynelesmis')
        self.assertEqual(x.notes[-1], 60)
        self.assertEqual(x.dates[-1], '2018-04-17 02:47:53')

    def testPostTypeData(self):
        x = final.GraphData()
        x.post_type_data('eddieredmaynelesmis')
        self.assertEqual(x.types, ['photo', 'text'])
        self.assertEqual(x.number, [49, 1])

    def testAskQuestionData(self):
        x = final.GraphData()
        x.ask_question_data()
        self.assertEqual(x.labels, ['Yes', 'No'])
        self.assertEqual(x.values, [1,0])

    def testNumberPostsData(self):
        x = final.GraphData()
        x.number_posts_data()
        self.assertEqual(x.accounts[0], 'eddieredmaynelesmis')
        self.assertEqual(x.posts_number[0], 508)



unittest.main(verbosity=2)
