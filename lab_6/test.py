import unittest
from main import *

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=10)
        self.ht.insert("ФА", "Футбол")
        self.ht.insert("ЦЖ", "Цирк")
        self.ht.insert("БА", "Баскетбол")

    def test_insert_and_search(self):
        self.assertEqual(self.ht.search("ФА"), "Футбол")
        self.assertEqual(self.ht.search("ЦЖ"), "Цирк")
        self.assertEqual(self.ht.search("БА"), "Баскетбол")

    def test_update(self):
        self.assertTrue(self.ht.update("ФА", "Новое описание"))
        self.assertEqual(self.ht.search("ФА"), "Новое описание")
        self.assertFalse(self.ht.update("НЕСУЩЕСТВУЕТ", "123"))

    def test_delete(self):
        self.assertTrue(self.ht.delete("ФА"))
        self.assertIsNone(self.ht.search("ФА"))
        self.assertEqual(self.ht.search("ЦЖ"), "Цирк")

    def test_collision_handling(self):
        index1 = self.ht.hash_function("ФА")
        index2 = self.ht.hash_function("ЦЖ")
        self.assertEqual(2, index2)

    def test_load_factor(self):
        occupied = sum(1 for bucket in self.ht.table if bucket is not None)
        self.assertAlmostEqual(self.ht.load_factor(), occupied / self.ht.size, places=2)

    def test_insert_duplicate(self):
        with self.assertRaises(ValueError):
            self.ht.insert("ФА", "Ещё одно значение")

if __name__ == "__main__":
    unittest.main()
