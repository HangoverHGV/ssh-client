import {useState} from "react";
import {invoke} from "@tauri-apps/api/core";
import "./App.css";

function App() {
    const [formData, setFormData] = useState({
        server: "",
        port: "22",
        privateKeyPath: "",
    });

    async function handleSubmit(e) {
        e.preventDefault();
        console.log(formData);
    }

    return (
        <main className="container">
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="server">Server:</label>
                    <input
                        type="text"
                        id="server"
                        value={formData.server}
                        onChange={(e) => setFormData({...formData, server: e.target.value})}
                    />
                    <label htmlFor="port">Port:</label>
                    <input
                        type="number"
                        id="port"
                        value={formData.port}
                        onChange={(e) => setFormData({...formData, port: e.target.value})}
                    />
                </div>
                <div className="full-width">
                    <label htmlFor="privateKeyPath">Private Key Path:</label>
                    <input
                        type="text"
                        id="privateKeyPath"
                        value={formData.privateKeyPath}
                        onChange={(e) => setFormData({...formData, privateKeyPath: e.target.value})}
                    />
                    <button type="button" onClick={() => invoke("open_file_dialog")}>Open File Dialog</button>
                </div>
                <button type="submit">Submit</button>
            </form>
        </main>
    );
}

export default App;