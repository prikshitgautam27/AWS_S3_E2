# ☁️ Cloud-Based File Management System (Replica over different region)

> **Secure, Scalable File Management with AWS S3 & Flask**

---

## 🏷️ Badges

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-black?style=flat-square&logo=flask)
![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20EC2-FF9900?style=flat-square&logo=amazon-aws)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## 📖 Project Overview

The **Cloud-Based File Management System** is a robust, enterprise-grade application that enables users to upload, download, manage, and replicate files securely on AWS cloud infrastructure. Built with Flask and powered by AWS S3 and EC2, this system provides a seamless experience for file management with advanced features like versioning, replication, and authentication.

### 🎯 Why Use This Project?

- ✅ **Scalable Infrastructure**: Leverage AWS to handle unlimited file storage
- ✅ **High Availability**: Automatic backup and replication across regions
- ✅ **Security First**: IAM-based authentication and encrypted storage
- ✅ **Easy Deployment**: Production-ready Flask application on EC2
- ✅ **User-Friendly Interface**: Intuitive web UI for file management

### ⭐ Key Features

| Feature | Description |
|---------|-------------|
| 📤 **File Upload** | Upload multiple files directly to AWS S3 with progress tracking |
| 📥 **File Download** | Download files with secure access control |
| 🔄 **S3 Replication** | Automatic file replication across multiple AWS regions |
| 📝 **S3 Versioning** | Track file versions and restore previous versions |
| 🔐 **Authentication** | User login with secure session management |
| 🚀 **Cloud Deployment** | Ready-to-deploy on AWS EC2 instances |
| 🛡️ **IAM Security** | Role-based access control and permissions |
| 📊 **File Metadata** | View file details, size, upload date, and storage location |

---

## 🏗️ Architecture Diagram

```mermaid
graph TB
    User["👤 User<br/>(Browser)"]
    Flask["🔷 Flask App<br/>(Route Handler)"]
    EC2["💻 EC2 Instance<br/>(Application Server)"]
    S3Primary["🗂️ S3 Bucket<br/>(Primary Region)"]
    S3Backup["🗂️ S3 Bucket<br/>(Backup Region)"]
    
    User -->|HTTP Request| Flask
    Flask -->|Process Request| EC2
    EC2 -->|Upload/Download| S3Primary
    S3Primary -->|Replicate| S3Backup
    S3Backup -->|Retrieve| EC2
    EC2 -->|HTTP Response| Flask
    Flask -->|Display Result| User
    
    style User fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
    style Flask fill:#2196F3,stroke:#333,stroke-width:2px,color:#fff
    style EC2 fill:#FF9800,stroke:#333,stroke-width:2px,color:#fff
    style S3Primary fill:#9C27B0,stroke:#333,stroke-width:2px,color:#fff
    style S3Backup fill:#9C27B0,stroke:#333,stroke-width:2px,color:#fff
