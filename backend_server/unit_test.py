import heapq
import unittest

from graph import Graph
from priority_queue import priority_queue
from main_server import app


class ServerTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test0_graph_initialization(self):
        """Test 1 ~ Test graph constructor."""
        vertices_number = 4
        edge_number = 5
        testGraph = Graph(vertices_number, edge_number)
        self.assertEqual(testGraph.vertices_count, vertices_number)
        self.assertEqual(testGraph.edges_count, edge_number)
        self.assertEqual(testGraph.adjacency_list, {})
        self.assertEqual(testGraph.vertices, [])
        self.assertEqual(testGraph.source, None)
        self.assertEqual(testGraph.dest, None)

    def test1_graph_addEdge(self):
        """Test 2 ~ Test add edge function."""
        vertices_number = 4
        edge_number = 5
        testGraph = Graph(vertices_number, edge_number)

        from_vertice = 0
        to_vertice = 1
        weight = 10
        adjacency_list = {from_vertice: {to_vertice: weight}, to_vertice: {}}
        vertices = [from_vertice, to_vertice]
        testGraph.addEdge(from_vertice, to_vertice, weight)

        self.assertEqual(testGraph.vertices_count, vertices_number)
        self.assertEqual(testGraph.edges_count, edge_number)
        self.assertEqual(testGraph.adjacency_list, adjacency_list)
        self.assertEqual(testGraph.vertices, vertices)
        self.assertEqual(testGraph.source, None)
        self.assertEqual(testGraph.dest, None)

    def test2_graph_set_source_dest(self):
        """Test 3 ~ Test set_source_dest function."""
        vertices_number = 4
        edge_number = 5
        testGraph = Graph(vertices_number, edge_number)

        source_vertice = 0
        destination_vertice = 1

        testGraph.set_source_dest(source_vertice, destination_vertice)

        self.assertEqual(testGraph.source, source_vertice)
        self.assertEqual(testGraph.dest, destination_vertice)

    def test3_priority_queue_initialization(self):
        """Test 4 ~ Test priority queue constructor."""
        testQueue = priority_queue()
        self.assertEqual(testQueue.queue, [])
        self.assertEqual(testQueue.length, 0)

    def test4_priority_queue_insert(self):
        """Test 5 ~ Test priority queue insert."""
        testQueue = priority_queue()

        distance_1 = 10
        vertex_1 = 0
        testQueue.insert(distance_1, vertex_1)

        self.assertEqual(testQueue.queue, [(distance_1, vertex_1)])
        self.assertEqual(testQueue.length, 1)

    def test5_priority_queue_heapify(self):
        """Test 6 ~ Test priority queue heapify."""
        testQueue = priority_queue()

        queue_length = 10
        expected_queue = []
        for i in range(queue_length - 1, -1, -1):
            heapq.heappush(expected_queue, (i + 1, i))
            testQueue.insert(i + 1, i)

        self.assertEqual(testQueue.queue, expected_queue)
        self.assertEqual(testQueue.length, queue_length)

    def test6_priority_queue_sort(self):
        """Test 7 ~ Test priority queue sort."""
        testQueue = priority_queue()

        queue_length = 10
        expected_queue = []
        for i in range(queue_length - 1, -1, -1):
            heapq.heappush(expected_queue, (i + 1, i))
            testQueue.insert(i + 1, i)

        sorted_expected_queue = sorted(expected_queue)
        sorted_return_queue = testQueue.sort()

        self.assertEqual(sorted_expected_queue, sorted_return_queue)
        self.assertEqual(testQueue.length, queue_length)

    def test7_priority_queue_remove(self):
        """Test 8 ~ Test priority queue remove."""
        testQueue = priority_queue()

        queue_length = 10
        expected_queue = []
        for i in range(queue_length - 1, -1, -1):
            heapq.heappush(expected_queue, (i + 1, i))
            testQueue.insert(i + 1, i)

        while len(expected_queue) > 0:
            heapq.heappop(expected_queue)
            testQueue.remove()
            self.assertEqual(testQueue.queue, expected_queue)
            self.assertEqual(testQueue.length, len(expected_queue))

        testQueue.remove()

        self.assertEqual(testQueue.queue, [])
        self.assertEqual(testQueue.length, 0)

    def test8_main_server_get_reccs(self):
        """Test 9 ~ Test main server's get recommendations function."""

        query = "Dijkstras Algorithm"
        response = self.app.get(
            "/get-recommendations/{}".format(query),
            mimetype='application/json')
        self.assertEqual(len(response.get_json()["result"]), 3)

    def test9_main_server_requests_methods(self):
        """Test 10 ~ Test a few main server's endpoints with various request methods."""

        query = "dijkstra"
        response = self.app.get("/get-decription/{}".format(query))
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/get-algorithm/{}".format(query))
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/get-algorithm/{}".format(query))
        self.assertEqual(response.status_code, 200)       
        response = self.app.get("/get-format/{}".format(query))
        self.assertEqual(response.status_code, 200)

        response = self.app.delete("/get-decription/{}".format(query))
        self.assertEqual(response.status_code, 405)
        response = self.app.delete("/get-algorithm/{}".format(query))
        self.assertEqual(response.status_code, 405)
        response = self.app.delete("/get-algorithm/{}".format(query))
        self.assertEqual(response.status_code, 405)       
        response = self.app.delete("/get-format/{}".format(query))
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ServerTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
