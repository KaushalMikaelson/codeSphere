# CodeSphere Local Development Setup: Windows 11 & XAMPP

This guide walks through configuring a local WordPress development environment using XAMPP (Apache + MariaDB + PHP) on Windows.

---

## 1. Prerequisites

1. **XAMPP for Windows** (PHP 8.2 or 8.3): Download from [Apache Friends](https://www.apachefriends.org/).
2. **Official WordPress Package**: Download `wordpress-6.x.zip` from [WordPress.org](https://wordpress.org/download/).
3. **Python 3.10+**: Installed on Windows and available in PowerShell (`python --version`).

---

## 2. Directory Placement & Web Root Setup

1. Start the **XAMPP Control Panel** as Administrator.
2. Start the **Apache** and **MySQL** modules.
3. Unzip the WordPress package into your XAMPP web root:
   ```
   C:\xampp\htdocs\codesphere\
   ```
4. Copy the CodeSphere custom theme:
   - Source: `e:\Projects\codeSphere\wordpress\wp-content\themes\codesphere`
   - Destination: `C:\xampp\htdocs\codesphere\wp-content\themes\codesphere`
5. Copy the CodeSphere plugin:
   - Source: `e:\Projects\codeSphere\wordpress\wp-content\plugins\codesphere-learning-links`
   - Destination: `C:\xampp\htdocs\codesphere\wp-content\plugins\codesphere-learning-links`

---

## 3. Database Creation (phpMyAdmin)

1. Open your browser and navigate to: `http://localhost/phpmyadmin/`.
2. Click **New** in the left sidebar.
3. Database name: `codesphere_db`.
4. Collation: `utf8mb4_unicode_ci`.
5. Click **Create**.

---

## 4. WordPress 5-Minute Installation

1. Navigate to `http://localhost/codesphere/` in your browser.
2. Select **English (United States)**.
3. Enter database connection details:
   - **Database Name:** `codesphere_db`
   - **Username:** `root`
   - **Password:** *(Leave blank for default XAMPP)*
   - **Database Host:** `localhost`
   - **Table Prefix:** `wp_`
4. Enter Site Details:
   - **Site Title:** `CodeSphere`
   - **Username:** *(Choose local admin username)*
   - **Password:** *(Choose secure password)*
   - **Your Email:** `admin@localhost`
5. Click **Install WordPress** and log in.

---

## 5. Enable Permalinks & Theme Activation

1. **Enable Clean URLs (Crucial for SEO):**
   - Go to **Settings > Permalinks**.
   - Under **Common Settings**, select **Post name** (`/%postname%/`).
   - Click **Save Changes**.
   - *(Note: Ensure Apache `mod_rewrite` is enabled in `C:\xampp\apache\conf\httpd.conf`)*.
2. **Activate CodeSphere Theme:**
   - Go to **Appearance > Themes**.
   - Hover over **CodeSphere** and click **Activate**.
3. **Activate Learning Links Plugin:**
   - Go to **Plugins > Installed Plugins**.
   - Click **Activate** under **CodeSphere Learning Links**.

---

## 6. One-Click Content Import (All 32 Articles)

1. In WordPress Admin, navigate to **Tools > Import**.
2. Under **WordPress**, click **Install Now** (or **Run Importer**).
3. Click **Browse** and select:
   ```
   e:\Projects\codeSphere\wordpress\content-import\codesphere-content.xml
   ```
4. Click **Upload file and import**.
5. Assign posts to your current admin user, check **Download and import file attachments**, and click **Submit**.
6. Visit `http://localhost/codesphere/` to verify all 4 clusters and 32 articles are live!
