# 🐇 Rabbit Hunter

**Rabbit Hunter** is a lightweight command-line tool for interacting with RabbitMQ queues. It supports secure and non-secure connections and lets you inspect, consume, requeue, reject, and purge messages.

It does **not** include any publishing, except for the `bulk_upload` method.

This tool is bundled as a single executable: `rabbit-hunter.exe`.

---

## 📦 Installation

### 📦 Install from GitHub

To install Rabbit Hunter directly from GitHub:

```bash
pip install git+https://github.com/swedwise/RabbitHunter.git
```

### 🛠️ Package with PyInstaller

Download or compile the tool using [PyInstaller](https://pyinstaller.org/) as follows:

```bash
pyinstaller --onefile --name rabbit-hunter rabbithunter/cli.py
```

This will generate `rabbit-hunter.exe` in the `dist/` folder.

## 🚀 Usage
Run the tool by executing:

```bash
rabbit-hunter.exe <command> [OPTIONS]
```

To get help on the main CLI or any subcommand:

```bash
rabbit-hunter.exe --help
rabbit-hunter.exe <command> --help
```

## 🧰 Available Commands

### 🔍 peek

Fetch one message without acknowledging it (non-destructive read).

```bash
rabbit-hunter.exe peek --host <host> --port <port> --username <user> --password <pass> --vhost <vhost> --queue <queue>
```

### ✅ pop

Fetch one message and acknowledge it (consumes the message).

```bash
rabbit-hunter.exe pop --host <host> --port <port> --username <user> --password <pass> --vhost <vhost> --queue <queue>
```

### 🔁 requeue

Fetch one message and reject it with requeue, returning it to the queue.

```bash
rabbit-hunter.exe requeue --host <host> --port <port> --username <user> --password <pass> --vhost <vhost> --queue <queue>
```

### 🚫 reject

Fetch one message and reject it without requeue, discarding it permanently.

```bash
rabbit-hunter.exe reject --host <host> --port <port> --username <user> --password <pass> --vhost <vhost> --queue <queue>
```
### 🧹 purge

Clear all messages from a queue. Prompts for confirmation ([y/N]).

```bash
rabbit-hunter.exe purge --host <host> --port <port> --username <user> --password <pass> --vhost <vhost> --queue <queue>
```
⚠️ **Use with caution — this operation is irreversible.**

### 🛑 drain 

The drain command is used to drain (i.e., read and remove) all messages from a specified queue and save them to a JSON file for later processing or bulk uploads.

```bash
rabbit-hunter.exe drain --host <host> --port <port> --username <username> --password <password> --vhost <vhost> --queue <queue> --output <output_file_path>
```

⚠️ **Use with caution — this operation is irreversible.**

### 🔄 bulk_upload

The bulk_upload command allows you to read messages from a JSON file and upload them to a specified queue or exchange in RabbitMQ. This operation preserves message properties like delivery mode, routing keys, and headers.

```bash
rabbit-hunter bulk_upload --host <host> --port <port> --username <username> --password <password> --vhost <vhost> [--queue <queue> | --exchange <exchange>] --input <input_file>
```

**Note:**

- `--queue`: (Optional) The target queue where messages will be uploaded. If specified, the queue name is used as the routing key.

- `--exchange`: (Optional) The target exchange. If specified, the `routing_key` from the message properties will be used to route the message to the correct destination.

## 🔐 SSL Support

- If port is 5671 (default SSL), SSL is enabled automatically.
- If port is 5672 (default non-SSL), no SSL is used.

No manual SSL toggle needed — the port determines the mode.

## 🛠 Example

```
rabbit-hunter.exe peek \
  --host message-broker.integration.regionstockholm.se \
  --port 5671 \
  --username pdms \
  --password mypassword \
  --vhost pdms \
  --queue takecare-juno
```

## 📄 License
MIT License

