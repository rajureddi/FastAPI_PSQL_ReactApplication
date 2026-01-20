import { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:5000";

function App() {
  const [products, setProducts] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState("");

  const [form, setForm] = useState({
    id: "",
    name: "",
    desc: "",
    price: ""
  });

  const [editing, setEditing] = useState(false);
  const [error, setError] = useState("");

  // ================= FETCH =================
  const fetchProducts = async () => {
    try {
      const res = await fetch(`${API}/all%20products`);
      const data = await res.json();
      setProducts(data);
      setFiltered(data);
    } catch {
      setError("Unable to fetch products");
    }
  };

  // ================= SEARCH =================
  const handleSearch = (e) => {
    const value = e.target.value.toLowerCase();
    setSearch(value);

    const result = products.filter(
      (p) =>
        p.name.toLowerCase().includes(value) ||
        p.id.toString().includes(value)
    );
    setFiltered(result);
  };

  // ================= FORM =================
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // ================= ADD =================
  const addProduct = async () => {
    setError("");

    if (!form.id || !form.name || !form.price) {
      setError("All fields are required");
      return;
    }

    if (isNaN(form.id) || isNaN(form.price)) {
      setError("ID and Price must be numbers");
      return;
    }

    try {
      const res = await fetch(`${API}/products`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: Number(form.id),
          name: form.name,
          desc: form.desc,
          price: Number(form.price)
        })
      });

      if (!res.ok) {
        const err = await res.json();
        if (res.status === 409) {
          setError(err.detail);
          return;
        }
        setError("Failed to add product");
        return;
      }

      resetForm();
      fetchProducts();
    } catch {
      setError("Server not reachable");
    }
  };

  // ================= UPDATE =================
  const updateProduct = async () => {
    setError("");

    if (!form.name || !form.price) {
      setError("Name and Price are required");
      return;
    }

    if (isNaN(form.price)) {
      setError("Price must be a number");
      return;
    }

    try {
      const res = await fetch(`${API}/products?id=${form.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: Number(form.id),
          name: form.name,
          desc: form.desc,
          price: Number(form.price)
        })
      });

      if (!res.ok) {
        setError("Failed to update product");
        return;
      }

      resetForm();
      fetchProducts();
    } catch {
      setError("Server not reachable");
    }
  };

  // ================= DELETE =================
  const deleteProduct = async (id) => {
    try {
      await fetch(`${API}/products?id=${id}`, { method: "DELETE" });
      fetchProducts();
    } catch {
      setError("Failed to delete product");
    }
  };

  // ================= EDIT =================
  const editProduct = (p) => {
    setForm(p);
    setEditing(true);
  };

  const resetForm = () => {
    setForm({ id: "", name: "", desc: "", price: "" });
    setEditing(false);
    setError("");
  };

  // ================= UI =================
  return (
    <div className="page">

      <div className="header">
        <h1>Product Trac</h1>
        <button onClick={fetchProducts}>Fetch</button>
      </div>

      <input
        className="search"
        placeholder="Search by id or name..."
        value={search}
        onChange={handleSearch}
      />

      <div className="card">
        <h2>{editing ? "Edit Product" : "Add Product"}</h2>

        {error && <div className="error">{error}</div>}

        <input
          name="id"
          placeholder="ID"
          value={form.id}
          onChange={handleChange}
          disabled={editing}
        />

        <input
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
        />

        <input
          name="desc"
          placeholder="Description"
          value={form.desc}
          onChange={handleChange}
        />

        <input
          name="price"
          placeholder="Price"
          value={form.price}
          onChange={handleChange}
        />

        {editing ? (
          <>
            <button onClick={updateProduct}>Update</button>
            <button className="cancel" onClick={resetForm}>Cancel</button>
          </>
        ) : (
          <button onClick={addProduct}>Add</button>
        )}
      </div>

      <div className="card">
        <h2>Products</h2>

        {filtered.length === 0 ? (
          <p className="empty">No products found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((p) => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.name}</td>
                  <td>{p.desc}</td>
                  <td>${p.price}</td>
                  <td>
                    <button onClick={() => editProduct(p)}>Edit</button>
                    <button
                      className="danger"
                      onClick={() => deleteProduct(p.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

    </div>
  );
}

export default App;
