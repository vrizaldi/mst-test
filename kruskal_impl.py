import matplotlib.pyplot as plt
from collections import defaultdict

# kelas graph


class Graph:
    def __init__(self, vertices):
        self.V = vertices  # jumlah vertex
        self.graph = []  # graph dalam adjacency matrix

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

        # gunakan union find agar pengecekan cepat

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot

        else:
            parent[yroot] = xroot
            rank[xroot] += 1

        # jalankan kruskal
    def calcMST(self):

        result = []

        i = 0  # indeks priority queue
        e = 0  # indeks result

        # sort priority queue berdasarkan weight dari edge
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []
        rank = []

        # subset V single elemen
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # lakukan sampai edge habis
        while e < self.V - 1:
            # ambil edge paling kecil selanjutnya
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # hanya simpan jika tidak terjadi cycle
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)

        return result


# Driver code
g = Graph(4)
g.addEdge(0, 1, 10)
g.addEdge(0, 2, 6)
g.addEdge(0, 3, 5)
g.addEdge(1, 3, 15)
g.addEdge(2, 3, 4)

g.calcMST()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])

city_x = []
city_y = []

# event handler untuk plot titik dengan mouse
dots = []
def onclick(event):
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))
    city_x.append(event.xdata)
    city_y.append(event.ydata)
    ln, = plt.plot(event.xdata, event.ydata, 'or')
    dots.append(ln)
    fig.canvas.draw()

# fungsi untuk menghitung jarak lurus (x1, y1) ke (x2, y2)
def calcDistance(x1, y1, x2, y2):
    return (x2 - x1)**2 + (y2 - y1)**2


connections = [] # menyimpan garis agar bisa dihapus
# event handler untuk keypress untuk menggambar edge
def press(event):
    # hapus semua garis
    for c in connections:
        c.remove()
    connections.clear()

    if(event.key == 'x'):
        # cari MST
        g = Graph(len(city_x))
        for i in range(len(city_x)):
            for j in range(len(city_x)):
                if(i != j):
                    # hanya buat edge jika bukan ke diri sendiri
                    g.addEdge(i, j, calcDistance(city_x[i], city_y[i], city_x[j], city_y[j]))
        res = g.calcMST()

        # gambar MST
        for u, v, _ in res:
            x = [city_x[u], city_x[v]]
            y = [city_y[u], city_y[v]]
            ln, = plt.plot(x, y, '-')  # agar bisa dihapus
            connections.append(ln)

    elif(event.key == ' '):
        # gambar seluruh koneksi
        for i in range(len(city_x)):
            for j in range(len(city_y)):
                if(i != j):
                    x = [city_x[i], city_x[j]]
                    y = [city_y[i], city_y[j]]
                    ln, = plt.plot(x, y, '-')  # agar bisa dihapus
                    connections.append(ln)

    elif(event.key == '.'):
        # hapus plot
        for d in dots:
            d.remove()
        dots.clear()
        city_x.clear()
        city_y.clear()

    else:
        return
    fig.canvas.draw()


# register event handler
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', press)

# gambar canvas
im = plt.imread('sumatra.gif')
implot = plt.imshow(im, extent=[0,10,0,10])
plt.show()
