# ☁️ MyCloudStorage — Distributed Cloud Storage System

A **fully functional, multi-user distributed cloud storage system** built from scratch with **Python (Flask)** and a **modern web interface**.

This mini-project demonstrates the **core principles of distributed cloud storage**, similar to services like **Dropbox** or **Google Drive**. It includes a complete **full-stack application** with a Python backend, a web-based frontend, and support for multiple users.

---

## ✨ Features

- 🔐 **User Authentication** – Secure signup and login system for multiple users.  
- 🧩 **File Sharding** – Large files are automatically broken down into smaller 1MB chunks.  
- 🌐 **Distributed Storage** – Central master node and multiple data nodes store chunks across machines.  
- ⚙️ **Full CRUD Operations** – Upload, view, download, and delete files easily.  
- 💻 **Modern Web UI** – Responsive, dark-themed, and user-friendly web interface.  
- 🔌 **API-Driven** – The frontend communicates with the backend using a well-defined REST API.

---

## 🚀 Project Demo

> *(Add a GIF or screenshots here showing the app in action!)*

- 🔑 **Login and Signup Flow**
- 📂 **User Dashboard and File Operations**

---

## 🏗️ Architecture Overview

The system follows a **client-server** and **master-worker distributed architecture**.

### 🧠 Master Node (`master_node.py`)

- Acts as the **central "brain"** of the system.  
- Handles **user accounts**, **authentication (signup/login)**, and **session tokens**.  
- Maintains all **metadata**:
  - Which user owns which files.
  - The list of chunks that make up each file.  
- Does **not** store any file data.  
- Orchestrates file operations by creating “plans” for clients.

---

### 💾 Data Node (`data_node.py`)

- Acts as a **storage worker**.  
- Responsible for **storing**, **retrieving**, and **deleting** file chunks via its API.  
- Has **no knowledge** of users or files — only raw chunks identified by unique IDs.

---

### 🖥️ Web Client (`index.html`)

- A **single-page application** (SPA) running entirely in the user's browser.  
- Provides UI for:
  - Signup/Login  
  - File Uploading, Viewing, and Deleting  
- Communicates directly with:
  - **Master Node** for instructions.
  - **Data Nodes** for actual data transfer.

---

## 🧰 Technology Stack

### Backend
- **Language:** Python 3  
- **Framework:** Flask  
- **CORS Handling:** Flask-CORS  

### Frontend
- **Structure:** HTML5  
- **Styling:** CSS3 (modern dark theme)  
- **Logic:** JavaScript (ES6+)

---

## ⚙️ Setup and Running the Project

### 🧱 Prerequisites
Make sure you have:
- **Python 3** installed  
- **pip** (Python package installer)

---

### 🔧 Installation

Open your terminal, navigate to the project directory, and install dependencies:

```bash
pip install Flask flask-cors
