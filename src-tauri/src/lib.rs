// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/

use std::process::Command;

#[tauri::command]
fn open_terminal() {
    if cfg!(target_os = "windows") {
        Command::new("cmd")
            .args(&["/C", "start", "cmd", "/K", "ssh hangoverhgv@192.168.0.114 -p 22 -i C:\\Users\\hango\\.ssh\\id_rsa_test"])
            .spawn()
            .expect("failed to execute process");
    } else if cfg!(target_os = "macos") {
        Command::new("open")
            .arg("-a")
            .arg("Terminal")
            .spawn()
            .expect("failed to execute process");
        Command::new("sh")
            .arg("-c")
            .arg("ssh hangoverhgv@192.168.0.114 -p 22 -i ~/.ssh/id_rsa_test")
            .spawn()
            .expect("failed to execute process");
    } else if cfg!(target_os = "linux") {
        Command::new("x-terminal-emulator")
            .arg("-e")
            .arg("sh -c 'ssh hangoverhgv@192.168.0.114 -p 22 -i ~/.ssh/id_rsa_test; exec bash'")
            .spawn()
            .expect("failed to execute process");
    }
}
#[tauri::command]
fn open_file_dialog() -> String{

}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![open_terminal])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
