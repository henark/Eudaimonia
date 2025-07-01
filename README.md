# Eudaimonia - A Platform for Human Flourishing

Eudaimonia is a plural social network designed for community-centric interaction and human flourishing. Built on the principles of "Faceted Identity" and community-first architecture, it reimagines social networking by prioritizing meaningful connections over engagement metrics.

## 🏗️ Architecture Overview

### Backend (Django + Django REST Framework)
- **Database**: PostgreSQL (with SQLite for development)
- **Authentication**: JWT-based with Django REST Framework Simple JWT
- **API**: RESTful API with comprehensive endpoints for all features
- **Models**: Community-centric design with LivingWorlds as primary entities

### Frontend (Next.js + TypeScript + Tailwind CSS)
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom theme support
- **State Management**: React Query for server state, local state for UI
- **Authentication**: Client-side token management

## 🚀 Features Implemented

### Core Features
- ✅ **User Authentication**: Registration, login, and JWT token management
- ✅ **Living Worlds**: Community spaces with themes and member management
- ✅ **Faceted Identity**: User profiles showing community affiliations and roles
- ✅ **Content Creation**: Posts within LivingWorlds with contextual theming
- ✅ **Friendship System**: Friend requests and relationship management
- ✅ **Community Membership**: Join worlds with roles and reputation tracking
- ✅ **Basic Governance**: Proposal and voting system (foundation for future DAO features)
- ✅ **AI Companion**: Contextual AI assistance (placeholder for OpenAI integration)

### Technical Features
- ✅ **Responsive Design**: Mobile-first approach with Tailwind CSS
- ✅ **Dynamic Theming**: LivingWorlds can have custom themes
- ✅ **Real-time Updates**: React Query for efficient data fetching and caching
- ✅ **Type Safety**: Full TypeScript implementation
- ✅ **API Documentation**: Comprehensive Django admin interface

## 📁 Project Structure

```
Eudaimonia/
├── docs/
│   └── Eudaimonia_Principles.md          # Project philosophy and roadmap
├── eudaimonia_backend/                   # Django backend
│   ├── eudaimonia_backend/              # Django project settings
│   │   ├── core/                            # Main Django app
│   │   │   ├── models.py                    # Database models
│   │   │   ├── serializers.py               # API serializers
│   │   │   ├── views.py                     # API views and ViewSets
│   │   │   ├── admin.py                     # Django admin configuration
│   │   │   ├── urls.py                      # Authentication URLs
│   │   │   └── api_urls.py                  # Main API URLs
│   │   ├── requirements.txt                 # Python dependencies
│   │   └── manage.py                        # Django management script
├── eudaimonia_frontend/                 # Next.js frontend
│   ├── app/                             # Next.js App Router
│   │   ├── dashboard/                   # Dashboard pages
│   │   │   ├── layout.tsx              # Dashboard layout
│   │   │   ├── page.tsx                # Main dashboard
│   │   │   └── worlds/                 # LivingWorld pages
│   │   ├── globals.css                 # Global styles
│   │   ├── layout.tsx                  # Root layout
│   │   └── page.tsx                    # Landing page
│   ├── components/                      # React components
│   │   ├── Header.tsx                  # Dashboard header
│   │   ├── Sidebar.tsx                 # Navigation sidebar
│   │   └── CreatePostForm.tsx          # Post creation form
│   ├── package.json                    # Node.js dependencies
│   ├── tailwind.config.js              # Tailwind configuration
│   └── tsconfig.json                   # TypeScript configuration
├── .cursor-rules                        # AI development guidelines
└── README.md                           # This file
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+ and pip
- Node.js 18+ and npm
- PostgreSQL (optional, SQLite used for development)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd eudaimonia_backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   OPENAI_API_KEY=your-openai-api-key  # Optional for AI Companion
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd eudaimonia_frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Token refresh
- `POST /api/auth/recovery/initiate/` - Social recovery (placeholder)

### Users
- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user details
- `GET /api/users/{id}/profile/` - Get faceted profile
- `GET /api/users/{id}/friends/` - Get user's friends

### Living Worlds
- `GET /api/worlds/` - List LivingWorlds
- `POST /api/worlds/` - Create LivingWorld
- `GET /api/worlds/{id}/` - Get world details
- `POST /api/worlds/{id}/join/` - Join world
- `GET /api/worlds/{id}/posts/` - Get world posts
- `GET /api/worlds/{id}/members/` - Get world members

### Posts
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create post
- `GET /api/posts/{id}/` - Get post details

### Friendships
- `GET /api/friendships/` - List friendships
- `POST /api/friendships/` - Send friend request
- `POST /api/friendships/{id}/accept/` - Accept friend request
- `POST /api/friendships/{id}/reject/` - Reject friend request
- `GET /api/friendships/pending/` - Get pending requests

### Governance
- `GET /api/proposals/` - List proposals
- `POST /api/proposals/` - Create proposal
- `GET /api/proposals/{id}/votes/` - Get proposal votes
- `POST /api/votes/` - Cast vote

### AI Companion
- `POST /api/companion/query/` - AI assistance (placeholder)

## 🎨 Design Philosophy

### Community-Centric Architecture
- **LivingWorlds as Primary Entities**: Communities are the central organizing principle
- **Contextual Content**: All posts are situated within specific LivingWorlds
- **Faceted Identity**: User identity emerges from community affiliations

### Faceted Identity Implementation
- Users have different roles and reputations across different LivingWorlds
- Identity is not monolithic but emerges from social connections
- Profile shows community memberships and roles

### Theming System
- Each LivingWorld can have custom theme data
- Dynamic theming applied to world pages
- Consistent design language with customizable colors

## 🔮 Future Roadmap

### Phase 1: Decentralization (Part IV Implementation)
- **IPFS Integration**: Decentralized content storage
- **ERC-4337 Account Abstraction**: Social recovery and faceted identity
- **Community Currencies**: ERC-1155 multi-token standard

### Phase 2: Advanced Governance
- **Polis Integration**: Consensus-finding and deliberation
- **Quadratic Funding**: Democratic resource allocation
- **Aragon DAO**: On-chain governance execution

### Phase 3: AI Enhancement
- **OpenAI Integration**: Full AI Companion functionality
- **Contextual Assistance**: AI that understands community context
- **Personalized Recommendations**: AI-driven content discovery

## 🤝 Contributing

This project follows the principles outlined in `docs/Eudaimonia_Principles.md`. When contributing:

1. Follow the community-centric architecture
2. Implement faceted identity concepts
3. Maintain the philosophical alignment with human flourishing
4. Use the `.cursor-rules` for AI-assisted development

## 📄 License

This project is part of the Eudaimonia ecosystem and follows the principles of plural social networks for human flourishing.

## 🙏 Acknowledgments

- **Georg Simmel**: "The Web of Group-Affiliations" for sociological framework
- **Orkut Dataset**: Empirical validation of community-centric architecture
- **Danielle Allen, E. Glen Weyl, Audrey Tang**: Plurality principles
- **Nassim Nicholas Taleb**: Antifragile concepts

---

*Built for human flourishing through meaningful community connections.* 