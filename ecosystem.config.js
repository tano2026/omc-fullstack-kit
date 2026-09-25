module.exports = {
  apps: [
    {
      name: "omc-telegram-gateway",
      script: "gateway/telegram_gateway.py",
      interpreter: "python",
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      env: {
        NODE_ENV: "production",
        PYTHONUNBUFFERED: "1"
      },
      error_file: "logs/telegram-error.log",
      out_file: "logs/telegram-out.log",
      time: true
    },
    {
      name: "omc-webhook-server",
      script: "gateway/webhook_server.py",
      interpreter: "python",
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      env: {
        NODE_ENV: "production",
        PYTHONUNBUFFERED: "1"
      },
      error_file: "logs/webhook-error.log",
      out_file: "logs/webhook-out.log",
      time: true
    }
  ]
};
