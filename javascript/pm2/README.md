# PM2 README

## **Introduction**
PM2 is a process manager for Node.js applications that helps keep applications alive, manage logs, and provide monitoring. It is widely used in production environments to ensure applications run continuously with automatic restarts in case of failures.

---

## **1. Installation**

### **1.1 Install PM2 Globally**
```sh
npm install -g pm2
```

### **1.2 Verify Installation**
```sh
pm list -g pm2
```

---

## **2. Basic Usage**

### **2.1 Start an Application**
```sh
pm start app.js
pm2 start app.js --name myApp
```

### **2.2 View Running Processes**
```sh
pm2 list
```

### **2.3 Restart an Application**
```sh
pm2 restart myApp
```

### **2.4 Stop an Application**
```sh
pm2 stop myApp
```

### **2.5 Delete an Application**
```sh
pm2 delete myApp
```

---

## **3. Advanced Features**

### **3.1 Process Monitoring**
```sh
pm2 monit
```

### **3.2 Log Management**
```sh
pm2 logs myApp
```

### **3.3 Auto-Restart on Crash**
PM2 automatically restarts applications on failure.

### **3.4 Running in Cluster Mode**
```sh
pm2 start app.js -i max
```

---

## **4. Managing PM2 Startup**

### **4.1 Generate Startup Script**
```sh
pm2 startup
```

### **4.2 Save Process List**
```sh
pm2 save
```

### **4.3 Resurrect Processes on Reboot**
```sh
pm2 resurrect
```

---

## **5. Best Practices**
- Use `pm2 save` to preserve process state.
- Regularly check logs with `pm2 logs`.
- Monitor resource usage via `pm2 monit`.
- Use cluster mode for high availability.

---

## **6. Learning Resources**
- **Official Documentation**: [https://pm2.keymetrics.io/docs/](https://pm2.keymetrics.io/docs/)
- **PM2 GitHub**: [https://github.com/Unitech/pm2](https://github.com/Unitech/pm2)

---

## **Conclusion**
PM2 is an essential tool for managing Node.js applications in production. It ensures applications run reliably and provides powerful monitoring and logging capabilities. 🚀
