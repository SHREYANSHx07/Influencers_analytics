# Influencer Marketing ROI Dashboard

A comprehensive dashboard for tracking influencer marketing performance, analyzing ROAS, and optimizing campaigns. Built with Django REST Framework backend and Streamlit frontend.

## 🌟 Features

### ✅ **COMPLETE FEATURE IMPLEMENTATION**

| **Feature** | **Status** | **Implementation Details** |
|-------------|------------|---------------------------|
| **1. Upload/Ingest Data** | ✅ **COMPLETE** | • Bulk CSV/JSON upload API<br>• Drag-and-drop frontend interface<br>• Data validation & error handling<br>• 55 sample records per file |
| **2. Track Performance** | ✅ **COMPLETE** | • Post engagement rate calculation<br>• Influencer performance metrics<br>• Real-time tracking API<br>• Performance analytics dashboard |
| **3. ROI/ROAS Calculation** | ✅ **COMPLETE** | • ROAS = total_revenue / total_payout<br>• Incremental ROAS analysis<br>• Multi-basis payout models<br>• Performance comparison metrics |
| **4. Advanced Filtering** | ✅ **COMPLETE** | • Platform filtering (Instagram, YouTube, TikTok)<br>• Category filtering (Fashion, Tech, Fitness, etc.)<br>• Gender filtering (Male, Female, Other)<br>• **Brand filtering** (Nike, Adidas, Apple, etc.)<br>• Date range filtering |
| **5. Insights & Analytics** | ✅ **COMPLETE** | • Top influencers ranking<br>• Best performing personas<br>• Poor ROI identification<br>• Platform performance analysis<br>• Category-based insights |

### 📊 Analytics & Calculations
- **ROAS Analysis**: Calculate Return on Ad Spend for campaigns
- **Incremental ROAS**: Compare campaigns with/without influencers
- **Top Influencers**: Rank by revenue, ROAS, engagement rate
- **Persona Analysis**: Analyze by category/gender/platform/brand
- **Trend Analysis**: Time-series revenue & orders per influencer
- **Payout Efficiency**: Orders per influencer, average payout metrics
- **Brand Performance**: Track performance by brand across campaigns

### 🎨 Dashboard Components
- **Campaign Performance**: Revenue tracking, order analysis, brand filtering
- **Influencer Comparison**: Performance metrics, engagement rates, platform analysis
- **Incremental ROAS**: Lift analysis, A/B testing insights
- **Payout Tracking**: 
  - Compensation management with multiple basis types (post, engagement, click, sale)
  - ROAS optimization with efficiency metrics
  - Platform and category payout analysis
  - Top ROAS performers visualization
  - Payout vs ROAS scatter plots
- **Insights & Innovation**: Predictive analytics, what-if scenarios

### 🔌 API Endpoints

#### Core Data Endpoints
- `GET /api/influencers/` - Influencer data with filtering
- `GET /api/posts/` - Post performance data
- `GET /api/tracking/` - Campaign tracking data with brand filtering
- `GET /api/payouts/` - Payout and compensation data

#### Analytics Endpoints
- `GET /api/influencers/top_performers/` - Top performing influencers
- `GET /api/tracking/roas_analysis/` - ROAS analysis by influencer
- `GET /api/payouts/summary/` - Payout summary statistics
- `GET /api/payouts/by_influencer/` - Payout analysis by influencer
- `GET /api/payouts/by_platform/` - Platform-based payout analysis
- `GET /api/payouts/by_category/` - Category-based payout analysis
- `GET /api/payouts/by_basis/` - Payout distribution by basis type
- `GET /api/payouts/efficiency_metrics/` - Payout efficiency metrics
- `GET /api/payouts/top_performers/` - Top ROAS performers

#### Data Management
- `POST /api/upload/` - Bulk CSV/JSON upload with validation
- `POST /api/clear/` - Clear database for testing

## 🏗️ Tech Stack

- **Backend**: Django REST Framework with advanced filtering
- **Frontend**: Streamlit with interactive visualizations
- **Database**: SQLite (development) / PostgreSQL (production)
- **Styling**: Amazon color palette (navy #146eb4, orange #ff9900)
- **Charts**: Plotly for interactive data visualization
- **Filtering**: Django-filter for advanced query parameters

## 📁 Project Structure

```
influencer_roi/
├── backend/                 # Django project
│   ├── config/             # Django settings
│   ├── influencers/        # Influencer & Post models
│   ├── tracking/          # TrackingData model with brand field
│   ├── payouts/           # Payout model with multiple basis types
│   ├── api/               # Bulk upload views
│   └── manage.py
├── frontend/              # Streamlit app
│   ├── app.py            # Main dashboard with brand filtering
│   └── .streamlit/       # Configuration
├── example_data/          # Sample CSV files with varied data
│   ├── influencers.csv   # 55 influencer records
│   ├── posts.csv         # 55 post records
│   ├── tracking.csv      # 55 tracking records with brand data
│   └── payouts.csv       # 55 payout records with multiple basis types
├── requirements.txt       # Dependencies
└── README.md
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd influencer_roi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Django Backend

```bash
cd backend

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start Django server
python manage.py runserver
```

### 3. Setup Streamlit Frontend

```bash
cd frontend

# Start Streamlit app
streamlit run app.py
```

### 4. Load Sample Data

Upload the example CSV files from `example_data/` using the dashboard's upload feature:

1. Go to "Insights & Innovation" tab
2. Upload `influencers.csv`, `posts.csv`, `tracking.csv`, `payouts.csv`
3. Select appropriate model type for each file

## 📊 Data Models

### Influencer
- `id` (UUID): Unique identifier
- `name` (CharField): Influencer's full name
- `category` (CharField): Content category (Fashion, Tech, Fitness, etc.)
- `gender` (CharField): Gender (male/female/other)
- `follower_count` (IntegerField): Number of followers
- `platform` (CharField): Primary platform (Instagram, YouTube, TikTok)

### Post
- `influencer` (ForeignKey): Associated influencer
- `platform` (CharField): Platform where post was made
- `date` (DateField): Post date
- `url` (URLField): Post URL
- `caption` (TextField): Post caption
- `reach` (IntegerField): Number of people who saw the post
- `likes` (IntegerField): Number of likes
- `comments` (IntegerField): Number of comments

### TrackingData
- `source` (CharField): Data source (Google Analytics, Shopify)
- `campaign` (CharField): Campaign name
- `brand` (CharField): Brand name (Nike, Adidas, Apple, etc.)
- `influencer` (ForeignKey): Associated influencer
- `user_id` (CharField): User identifier
- `product` (CharField): Product name/SKU
- `date` (DateField): Tracking date
- `orders` (IntegerField): Number of orders
- `revenue` (DecimalField): Revenue generated

### Payout
- `influencer` (ForeignKey): Associated influencer
- `basis` (CharField): Payout basis (post, engagement, click, sale)
- `rate` (DecimalField): Rate per post/engagement/click/sale
- `orders` (IntegerField): Number of orders
- `total_payout` (DecimalField): Total payout amount
- `payout_date` (DateField): Date of payout

## 🔧 Configuration

### Django Settings
- Database: SQLite for development, PostgreSQL for production
- CORS: Enabled for Streamlit frontend
- REST Framework: Pagination, filtering, search
- Advanced filtering: Platform, category, gender, brand, date range

### Streamlit Configuration
- Theme: Amazon color palette
- Layout: Wide layout with sidebar filters
- Charts: Plotly for interactive visualizations
- Filters: Platform, category, gender, brand, date range

## 📈 Analytics Features

### ROAS Calculation
```python
ROAS = total_revenue / total_payout
```

### Engagement Rate
```python
engagement_rate = (likes + comments) / reach * 100
```

### Payout Efficiency Metrics
- **Average Payout per Order**: Total payout / total orders
- **Average Payout per Influencer**: Total payout / number of influencers
- **Payout Efficiency**: Orders per influencer
- **Overall ROAS**: Total revenue / total payout

### Incremental ROAS
- Compare campaigns with/without influencer participation
- Lift analysis for campaign effectiveness
- A/B testing insights

## 🎯 Advanced Filtering

### Platform Filtering
- Instagram, YouTube, TikTok, Twitter, LinkedIn
- Platform-specific performance analysis
- Cross-platform comparison

### Category Filtering
- Fashion, Tech, Fitness, Beauty, Food, Travel
- Category-based ROI analysis
- Best performing categories

### Gender Filtering
- Male, Female, Other
- Gender-based performance insights
- Demographic analysis

### Brand Filtering
- Nike, Adidas, Apple, Samsung, Coca-Cola, Pepsi, McDonald's, KFC
- Brand-specific campaign tracking
- Cross-brand performance comparison

### Date Range Filtering
- Custom date ranges for analysis
- Time-series performance tracking
- Seasonal trend analysis

## 🚀 Innovation Ideas

### Predictive Analytics
- **Next Best Influencer**: ML model to predict top performers
- **Engagement Prediction**: Forecast engagement rates
- **ROAS Forecasting**: Predict campaign performance

### What-If Scenarios
- **Rate Optimization**: Adjust payout rates, predict ROI impact
- **Campaign Planning**: Test different influencer combinations
- **Budget Allocation**: Optimize spend across influencers

### Smart Alerts
- **Performance Monitoring**: Real-time campaign tracking
- **ROAS Thresholds**: Alert on underperforming campaigns
- **Engagement Drops**: Flag declining engagement rates

## 🔍 API Usage Examples

### Get Influencers with Filters
```bash
curl "http://localhost:8000/api/influencers/?platform=instagram&category=Fashion&gender=female&brand=nike"
```

### Get Top Performers
```bash
curl "http://localhost:8000/api/influencers/top_performers/?start_date=2024-01-01&end_date=2024-12-31"
```

### Get ROAS Analysis
```bash
curl "http://localhost:8000/api/tracking/roas_analysis/?start_date=2024-01-01&end_date=2024-01-31&brand=apple"
```

### Get Payout Analysis by Platform
```bash
curl "http://localhost:8000/api/payouts/by_platform/?start_date=2024-01-01&end_date=2024-12-31"
```

### Get Payout Efficiency Metrics
```bash
curl "http://localhost:8000/api/payouts/efficiency_metrics/?platform=instagram&category=Fashion"
```

### Upload Data
```bash
curl -X POST "http://localhost:8000/api/upload/" \
  -F "file=@influencers.csv" \
  -F "model_type=influencers"
```

### Clear Database (Testing)
```bash
curl -X POST "http://localhost:8000/api/clear/" \
  -H "Content-Type: application/json"
```

## 🛠️ Development

### Adding New Models
1. Create model in appropriate app
2. Add serializer in `serializers.py`
3. Create ViewSet in `views.py`
4. Register in `config/urls.py`
5. Run migrations

### Adding New Analytics
1. Add calculation method to model
2. Create API endpoint in ViewSet
3. Add visualization in Streamlit app
4. Update documentation

### Adding New Filters
1. Add filter field to model
2. Update ViewSet filterset_fields
3. Add filter to frontend sidebar
4. Update API documentation

## 📝 Sample Data Features

### Varied Payout Basis Types
- **post**: $100 per post
- **engagement**: $50 per engagement
- **click**: $25 per click
- **sale**: $200 per sale

### Brand Distribution
- Nike, Adidas, Apple, Samsung
- Coca-Cola, Pepsi, McDonald's, KFC
- Cross-brand performance analysis

### Platform Diversity
- Instagram, YouTube, TikTok
- Platform-specific engagement rates
- Cross-platform comparison

## 🔒 Security Considerations

- CORS configured for development
- Input validation on all endpoints
- File upload restrictions
- SQL injection protection via Django ORM
- Data privacy maintained in all operations

## 📊 Performance Optimization

- Database indexing on frequently queried fields
- API pagination for large datasets
- Caching for summary statistics
- Efficient queries with select_related/prefetch_related
- Optimized aggregations with proper output_field specifications

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request



---

**Built with ❤️ for influencer marketing analytics**

