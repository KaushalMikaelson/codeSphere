# CodeSphere Production Deployment Guide: Ubuntu 24.04 LTS, Nginx, PHP-FPM, MariaDB & Cloudflare

This document provides a production-grade, reproducible deployment guide for hosting **CodeSphere** on an Ubuntu 24.04 LTS VPS with Nginx, PHP 8.3-FPM, MariaDB, Certbot SSL, and Cloudflare CDN proxy.

> **Important Deployment Policy:**  
> Use the placeholders below throughout setup:
> - Domain: `example.com` / `codesphere.yourdomain.edu`
> - Server IP: `203.0.113.10`
> - Database Name: `codesphere_prod`
> - Database User: `codesphere_user`
> - Database Password: `YOUR_SECURE_DB_PASSWORD`
> 
> *Never claim a server or certificate is live unless verified against the actual infrastructure.*

---

## 1. Prerequisites and System Updates

Connect to your Ubuntu 24.04 LTS server via SSH:
```bash
ssh user@203.0.113.10
sudo apt update && sudo apt upgrade -y
sudo apt install -y ufw curl wget unzip git fail2ban
```

Configure UFW Firewall:
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status verbose
```

---

## 2. MariaDB Database Installation & Hardening

Install MariaDB server:
```bash
sudo apt install -y mariadb-server
sudo systemctl enable --now mariadb
```

Secure the installation:
```bash
sudo mariadb-secure-installation
```
*(Respond `Y` to remove anonymous users, disallow remote root login, and remove test databases).*

Create the database and dedicated user:
```bash
sudo mariadb -u root -p
```
```sql
CREATE DATABASE codesphere_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'codesphere_user'@'localhost' IDENTIFIED BY 'YOUR_SECURE_DB_PASSWORD';
GRANT ALL PRIVILEGES ON codesphere_prod.* TO 'codesphere_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 3. Install Nginx, PHP 8.3-FPM, and Required Extensions

Ubuntu 24.04 LTS packages PHP 8.3 by default:
```bash
sudo apt install -y nginx php8.3-fpm php8.3-mysql php8.3-curl php8.3-gd php8.3-mbstring \
    php8.3-xml php8.3-xmlrpc php8.3-soap php8.3-intl php8.3-zip php8.3-bcmath php8.3-imagick
```

Optimize PHP-FPM configuration in `/etc/php/8.3/fpm/php.ini`:
```ini
upload_max_filesize = 64M
post_max_size = 64M
memory_limit = 256M
max_execution_time = 300
date.timezone = Asia/Kolkata
```
Restart PHP-FPM:
```bash
sudo systemctl restart php8.3-fpm
```

---

## 4. Install WordPress Core and Deploy CodeSphere Theme & Plugin

Create the web root directory:
```bash
sudo mkdir -p /var/www/codesphere
sudo chown -R $USER:$USER /var/www/codesphere
cd /var/www/codesphere
```

Download and unpack official WordPress:
```bash
wget https://wordpress.org/latest.tar.gz
tar -xzvf latest.tar.gz --strip-components=1
rm latest.tar.gz
```

Copy the CodeSphere custom theme and plugin from this repository:
```bash
# From workspace / repository root
cp -r wordpress/wp-content/themes/codesphere /var/www/codesphere/wp-content/themes/
cp -r wordpress/wp-content/plugins/codesphere-learning-links /var/www/codesphere/wp-content/plugins/
```

Set correct Linux ownership and permissions (WordPress security standard):
```bash
sudo chown -R www-data:www-data /var/www/codesphere
sudo find /var/www/codesphere/ -type d -exec chmod 755 {} \;
sudo find /var/www/codesphere/ -type f -exec chmod 644 {} \;
```

Create `wp-config.php`:
```bash
sudo -u www-data cp /var/www/codesphere/wp-config-sample.php /var/www/codesphere/wp-config.php
```
Configure database credentials and unique security salts in `/var/www/codesphere/wp-config.php`:
```php
define( 'DB_NAME', 'codesphere_prod' );
define( 'DB_USER', 'codesphere_user' );
define( 'DB_PASSWORD', 'YOUR_SECURE_DB_PASSWORD' );
define( 'DB_HOST', 'localhost' );
define( 'DB_CHARSET', 'utf8mb4' );
define( 'DB_COLLATE', '' );

// Retrieve unique salts from https://api.wordpress.org/secret-key/1.1/salt/
define( 'FS_METHOD', 'direct' );
define( 'WP_POST_REVISIONS', 5 );
define( 'EMPTY_TRASH_DAYS', 7 );
```

---

## 5. Nginx Server Block Configuration

Create `/etc/nginx/sites-available/codesphere.conf`:
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name codesphere.example.com;

    root /var/www/codesphere;
    index index.php index.html;

    access_log /var/log/nginx/codesphere_access.log;
    error_log /var/log/nginx/codesphere_error.log;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip Compression for Fast SEO Loading
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Clean Permalinks
    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    # Pass PHP scripts to PHP-FPM socket
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    # Deny access to sensitive files
    location ~* /(?:uploads|files)/.*\.php$ {
        deny all;
    }
    location ~ /\.ht {
        deny all;
    }
    location = /wp-config.php {
        deny all;
    }

    # Static Assets Caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|webp|svg|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Allow robots.txt and sitemap.xml
    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }
}
```

Enable site and test configuration:
```bash
sudo ln -s /etc/nginx/sites-available/codesphere.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 6. HTTPS Setup via Certbot & Cloudflare Full (Strict) SSL

### Step 1: Cloudflare DNS Configuration
1. Log in to Cloudflare Dashboard.
2. Under DNS records for your domain, add:
   - **Type:** `A`
   - **Name:** `codesphere` (or `@` for apex)
   - **IPv4 address:** `203.0.113.10`
   - **Proxy status:** Proxied (Orange cloud)

### Step 2: Issue Origin / Let's Encrypt Certificate
Install Certbot for Nginx:
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d codesphere.example.com
```

Test automatic renewal:
```bash
sudo certbot renew --dry-run
```

### Step 3: Cloudflare SSL/TLS Settings
1. Navigate to **Cloudflare > SSL/TLS > Overview**.
2. Select encryption mode: **Full (strict)**.
3. Under **Edge Certificates**, enable:
   - **Always Use HTTPS**
   - **Minimum TLS Version: TLS 1.2** (TLS 1.3 enabled)
   - **Automatic HTTPS Rewrites**

---

## 7. Service Verification & Post-Deployment Checklist

Execute these checks to verify healthy deployment:

```bash
# 1. Verify Nginx and PHP-FPM service status
sudo systemctl status nginx --no-pager
sudo systemctl status php8.3-fpm --no-pager
sudo systemctl status mariadb --no-pager

# 2. Check HTTP 200 response and SSL certificate
curl -I https://codesphere.example.com/

# 3. Verify robots.txt and sitemap
curl -s https://codesphere.example.com/robots.txt
curl -sI https://codesphere.example.com/sitemap.xml
```

---

## 8. Backup and Disaster Recovery Procedure

### Automated Database Backup Script (`/usr/local/bin/backup-codesphere.sh`):
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/codesphere"
DATE=$(date +'%Y-%m-%d_%H%M%S')
mkdir -p "$BACKUP_DIR"

# Dump database
mysqldump -u codesphere_user -p'YOUR_SECURE_DB_PASSWORD' codesphere_prod | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Archive uploads and theme
tar -czf "$BACKUP_DIR/wp-content_$DATE.tar.gz" -C /var/www/codesphere wp-content

# Keep 14 days of backups
find "$BACKUP_DIR" -type f -mtime +14 -delete
```
Make executable and schedule in crontab (`crontab -e`):
```cron
0 2 * * * /usr/local/bin/backup-codesphere.sh > /dev/null 2>&1
```

### Restore Procedure:
```bash
gunzip < /var/backups/codesphere/db_YYYY-MM-DD.sql.gz | mariadb -u codesphere_user -p codesphere_prod
tar -xzf /var/backups/codesphere/wp-content_YYYY-MM-DD.tar.gz -C /var/www/codesphere/
```
