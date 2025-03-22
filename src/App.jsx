import {useState, useEffect} from "react";
import {invoke} from "@tauri-apps/api/core";
import {open} from "@tauri-apps/plugin-dialog";
import "./App.css";
import {homeDir} from "@tauri-apps/api/path";
import { Menu, MenuItem, MenuButton } from '@szhsin/react-menu';
import '@szhsin/react-menu/dist/index.css';


function App() {
    const [formData, setFormData] = useState({
        name: "",
        server: "",
        port: "22",
        privateKeyPath: "",
    });
    const [settings, setSettings] = useState(null);
    const [configs, setConfigs] = useState(null);

    useEffect(() => {
        loadSettings();
    }, []);

    async function loadSettings() {
        setConfigs(await invoke("get_json_configs", {configType: "configs"}));
        setSettings(await invoke("get_json_configs", {configType: "settings"}));
    }

    async function populateFilePath() {
        const homeDirPath = await homeDir();
        const file = await open({
            multiple: false,
            directory: false,
            defaultPath: `${homeDirPath}/.ssh`,
        });
        if (file) {
            setFormData({...formData, privateKeyPath: file});
        }
    }

    async function saveConfigs() {
        const existingConfigIndex = configs.findIndex(config => config.name === formData.name);

        if (existingConfigIndex !== -1) {
            const shouldOverwrite = await confirm("Configuration with this name already exists. Do you want to overwrite it?");
            if (!shouldOverwrite) {
                return;
            }
            const updatedConfigs = [...configs];
            updatedConfigs[existingConfigIndex] = formData;
            setConfigs(updatedConfigs);
            await invoke("save_json_config", {configType: "configs", data: updatedConfigs});
        } else {
            const updatedConfigs = [...configs, formData];
            setConfigs(updatedConfigs);
            await invoke("save_json_config", {configType: "configs", data: updatedConfigs});
        }
        setFormData(formData);
        document.getElementById("connectionSelect").value = formData.name;
    }

    async function deleteConfigs() {
        const shouldDelete = await confirm("Are you sure you want to delete this configuration?");
        if (!shouldDelete) {
            return;
        }
        const updatedConfigs = configs.filter(config => config.name !== formData.name);
        setConfigs(updatedConfigs);
        await invoke("save_json_config", {configType: "configs", data: updatedConfigs});
        setFormData({
            name: "",
            server: "",
            port: "22",
            privateKeyPath: "",
        });
        document.getElementById("connectionSelect").value = "Select a connection";
    }

    async function connect() {
        await invoke("open_terminal", {
            server: formData.server,
            port: formData.port,
            key: formData.privateKeyPath,
        });
    }

    return <>
        <nav>
            <Menu menuButton={<MenuButton className="btn">Edit</MenuButton>}>
                <MenuItem>Settings</MenuItem>
            </Menu>
        </nav>
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
                    <button type="button" className="btn" onClick={populateFilePath}>Open File Dialog</button>
                </div>
                <div>
                    <label htmlFor="connectionName">Connection Name:</label>
                    <input type="text" id="connectionName" value={formData.name}
                           onChange={(e) => setFormData({...formData, name: e.target.value})}/>
                    <button type="button" className="btn" onClick={saveConfigs}>Save</button>
                    <button type="button" className="btn btn-danger" onClick={deleteConfigs}>Delete</button>
                </div>
                <div className="full-width">
                    <label htmlFor="connectionName">Saved Connections:</label>
                    <select id="connectionSelect" onChange={(e) => {
                        const selectedConfig = configs.find(config => config.name === e.target.value);
                        if (selectedConfig) {
                            setFormData(selectedConfig);
                        } else {
                            setFormData({
                                name: "",
                                server: "",
                                port: "22",
                                privateKeyPath: "",
                            });
                        }
                    }}>
                        <option>Select a connection</option>
                        {configs && configs.map(config => (
                            <option key={config.name}>{config.name}</option>
                        ))}
                    </select>
                </div>
                <button type="submit" className="btn btn-success">Connect</button>
            </form>
        </main>
    </>;
}

export default App;