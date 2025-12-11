import networkx as nx
import matplotlib.pyplot as plt
import time 

def getchild(p_idx, tree):
    p_name = tree[p_idx]["name"]
    c_name_queue = []
    parent = list()
    depth = tree[p_idx]["depth"] + 1
    log = 1
    
    while True:
        input_children = input("Siapakah anak-anak %s? (Pisahkan dengan spasi, ENTER untuk selesai): " % p_name).strip()
        
        if not input_children:
            break
        
        current_children = input_children.split()
        
        all_unique = True
        temp_queue = []
        for c_name in current_children:
            c_name = c_name.strip()
            if not c_name:
                continue

            if getindex(c_name, tree) is not None:
                print(f"Nama '{c_name}' sudah ada. Mohon masukkan nama yang unik!")
                all_unique = False
                break
            temp_queue.append(c_name)

        if all_unique:
            c_name_queue.extend(temp_queue)
            break

    if len(c_name_queue) == 0:
        return

    parent = [p_idx]
    while depth >= 1 << log:
        parent_of_prev = tree[parent[log-1]].get("parent")
        if parent_of_prev and len(parent_of_prev) >= log:
             parent.append(parent_of_prev[log-1])
        else:
             if parent[log-1] == 0:
                parent.append(0)
             else:
                break 

        log += 1
        
    for c_name in c_name_queue:
        tree.append({"name": c_name,
                     "parent": parent,
                     "depth": depth})
        getchild(len(tree) - 1, tree)

    return


def getindex(name, tree):
    for i in range(len(tree)):
        if tree[i]["name"] == name:
            return i

    return None


def lca(a, b, tree):
    node_a = tree[a]
    node_b = tree[b]
    log = 0

    if a == 0 or b == 0:
        return tree[0]["name"]

    if node_a["depth"] < node_b["depth"]:
        temp = a
        a = b
        b = temp
        node_a = tree[a]
        node_b = tree[b]

    diff = node_a["depth"] - node_b["depth"]

    log = 0
    while diff > 0:
        if diff & 1:
            if log >= len(node_a["parent"]): 
                 a = 0
                 node_a = tree[a]
                 break 

            a = node_a["parent"][log]
            node_a = tree[a]

        diff >>= 1
        log += 1

    if a == b:
        return tree[a]["name"]

    i = len(node_a["parent"]) - 1
    
    while i >= 0:
        if node_a["parent"][i] != node_b["parent"][i]:
            a = node_a["parent"][i]
            b = node_b["parent"][i]
            node_a = tree[a]
            node_b = tree[b]
        
        if i == 0 and node_a["parent"][i] != node_b["parent"][i]:
            a = node_a["parent"][i]
            
        i -= 1

    return tree[tree[a]["parent"][0]]["name"]


def visualize_tree(tree):
    G = nx.DiGraph()
    labels = {}

    for i in range(len(tree)):
        labels[i] = tree[i]["name"]
        G.add_node(i)

        if tree[i]["parent"] is not None and len(tree[i]["parent"]) > 0:
            parent_idx = tree[i]["parent"][0]
            if parent_idx != i:
                G.add_edge(parent_idx, i)
        
    

    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    except ImportError:
        pos = nx.spring_layout(G)


    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, labels=labels, with_labels=True,
            node_size=2500, node_color="#ADD8E6",
            font_size=10, font_weight="bold",
            arrows=True, arrowsize=20, edge_color="gray")
    plt.title("Visualisasi Family Tree")
    
    plt.ion()
    plt.show(block=False) 
    plt.pause(0.1)


def main():
    prompt = "Siapakah nenek moyang (root/paling atas)?: "
    tree = list()

    print("🌳 LOWEST ANCESTOR FINDER 🌳")
    
    root_name = input(prompt).strip()
    while not root_name or getindex(root_name, tree) is not None:
         if not root_name:
             root_name = input("Nama nenek moyang tidak boleh kosong. " + prompt).strip()
         elif getindex(root_name, tree) is not None:
              print(f"Nama '{root_name}' sudah ada. Mohon masukkan nama yang unik!")
              root_name = input(prompt).strip()


    tree.append({"name": root_name,
                 "parent": None,
                 "depth": 0})
    
    getchild(0, tree)
    
    print("\nMenampilkan visualisasi tree...")
    visualize_tree(tree) 

    print("\n--- 🔎 PENCARIAN LOWEST COMMON ANCESTOR (LCA) 🔎 ---")
    print("Masukkan dua nama dipisahkan oleh spasi (misalnya: Budi Siti).")
    print("Tekan ENTER tanpa input untuk keluar dari kueri.")

    while True:
        query = input("Masukkan pasangan nama (Nama1 Nama2): ").strip()

        if not query:
            print("Terima kasih, program LCA selesai.")
            break

        names = query.split()

        if len(names) != 2:
            print("❌ Input tidak valid. Harap masukkan dua nama dipisahkan spasi.")
            continue

        name_a, name_b = names[0], names[1]

        idx_a = getindex(name_a, tree)
        idx_b = getindex(name_b, tree)

        if idx_a is None or idx_b is None:
            missing_names = []
            if idx_a is None:
                missing_names.append(name_a)
            if idx_b is None:
                missing_names.append(name_b)

            print(f"❌ Nama-nama berikut tidak ditemukan: {', '.join(missing_names)}")
            continue

        if idx_a == idx_b:
            print(f"Orang yang sama ('{name_a}'). LCA-nya adalah diri sendiri: {name_a}")
            continue
            
        ancestor_name = lca(idx_a, idx_b, tree)

        print(f"{name_a} dan {name_b} memiliki hubungan darah pada {ancestor_name}")
        
    plt.close('all')

if __name__ == "__main__":
    main()