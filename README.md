# pyytsync: Synchronized YouTube Viewing Experience

**pyytsync** is a sleek and user-friendly web application designed to synchronize YouTube video playback across multiple sessions. Whether you're hosting a virtual movie night or coordinating a watch party, **pyytsync** delivers a seamless group viewing experience.

![Enhanced sample image](sample.png)

## :sparkles: Features
- **Responsive UI**: Utilizing Bootstrap 5 and JavaScript for a smooth and swift user experience.
- **Video Queue Management**: Effortlessly add, delete, and reorder videos with intuitive Drag & Drop.
- **Docker Deployment**: Quick and straightforward setup using Docker and Docker-compose.
- **Single Room Focus**: Optimized for private sessions, supporting a single "Room" of clients.

## :warning: Note
- **pyytsync** is tailored for private gatherings. Hosting a public instance is not advised.

## :rocket: Quick Installation
1. Clone the repository: `git clone git@github.com:rndxelement/pyytsync.git`
2. Configure the environment: Copy `.env.dev` to `.env` and update the variables.
3. Set the YouTube Data API key in `pyytsync/pyytsync/settings.py`.

## :construction_worker: Building and Running
Launch your private **pyytsync** instance with a simple command: `docker-compose build && docker-compose up -d`

## :gem: Optional Browser Extension
Enhance your experience with our custom browser extension. Right-click on YouTube videos and directly add them to your **pyytsync** queue. 

**Setup**:
1. Navigate to `browser_extension`.
2. Replace `<pyytsync-instance>` with your domain (e.g., `your-domain.xyz`).
3. Enable the unsigned extension through your browser's developer options.

## :heart: Contribute and Collaborate
Join us in elevating **pyytsync**! Whether it's documentation, front-end enhancements, bug reports, or feature ideas - your contributions are immensely appreciated.

### Areas for Enhancement:
- Enhancing client synchronization scripts.
- Streamlining the deployment process.
- Front-end improvements and refactoring.
