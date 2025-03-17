import {useState, useEffect} from "react";
import {invoke} from "@tauri-apps/api/core";
import {open} from "@tauri-apps/plugin-dialog";
import "./App.css";

function App() {
    const [formData, setFormData] = useState({
        server: "",
        port: "22",
        privateKeyPath: "",
    });

    async function populateFilePath() {
        const file = await open({
            multiple: false,
            directory: false,
            filters: [{name: "All Files", extensions: ["*"]}],
        });
        if (file) {
            setFormData({...formData, privateKeyPath: file});
        }
    }

    async function connect() {
        console.log("Connecting to server...");
        await invoke("open_terminal", {
            server: formData.server,
            port: formData.port,
            key: formData.privateKeyPath,
        });
    }

    return (
        <main className="container">
            <form onSubmit={(e) => {
                e.preventDefault();
                connect();
            }}>
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
                    <button type="button" onClick={populateFilePath}>Open File Dialog</button>
                </div>
                <button type="submit">Connect</button>
            </form>
        </main>
    );
}

export default App;