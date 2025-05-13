# Microservices Architecture Report

## Feature Decomposition into Microservices

The application has been decomposed into the following microservices, with each feature mapped to its implementing service(s):

| Feature | Microservice(s) Involved | Database Used | Why Database Needed |
|---------|--------------------------|---------------|----------------------|
| 1. User creation | User Service | PostgreSQL | Persistent storage of user credentials and profiles |
| 2. Add friends | User Service | PostgreSQL | Persistent storage of friend relationships |
| 3. Watch movies | Watch History Service | PostgreSQL | Persistent storage of watch history with timestamps |
| 4. Rate movies | Rating Service | PostgreSQL | Persistent storage of ratings and reactions |
| 5. View friend's ratings | Rating Service | PostgreSQL | Retrieval of historical rating data |
| 6. Agree/disagree with ratings | Rating Service | PostgreSQL | Persistent storage of rating reactions |
| 7. Top-rated recommendations | Recommendation Service | None | Aggregates data from other services in real-time |
| 8. Friends' unseen recommendations | Recommendation Service | None | Computes recommendations from live queries |
| 9. Newsfeed of friends' activity | Newsfeed Service | None | Aggregates data from other services on demand |
| 10. Full movie list | Movie Service | CSV File | Static movie dataset loaded into memory |

### Database Usage Rationale:

**Services With Databases:**
1. **User Service**
   - Database: PostgreSQL
   - Why: Critical for persistent storage of sensitive user data and relationships that must survive restarts

2. **Watch History Service**  
   - Database: PostgreSQL  
   - Why: Requires durable storage of temporal data with precise timestamps for activity tracking

3. **Rating Service**  
   - Database: PostgreSQL  
   - Why: Needs ACID compliance for rating updates and reaction tracking

**Services Without Databases:**
1. **Recommendation Service**  
   - Why: Stateless computation engine that aggregates data from other services in real-time

2. **Newsfeed Service**  
   - Why: Aggregates fresh data from Watch History without needing local persistence

3. **Movie Service**  
   - Storage: CSV file in memory  
   - Why: Static dataset that doesn't require write operations or complex queries

### Detailed Feature-Service Mapping:

1. **User Service (5001)**
   - Feature 1: User creation (`POST /users/`)
   - Feature 2: Add friends (`POST /users/<id>/friends/`)
   - Core user management isolated for reliability

2. **Watch History Service (5002)**
   - Feature 3: Watch movies (`POST /watch_history/<user>/<movie>/`)
   - Dedicated service for viewing history tracking

3. **Rating Service (5003)**
   - Feature 4: Rate movies (`POST /ratings/<user>/<movie>/`)
   - Feature 5: View friend's ratings (`GET /ratings/<user>/`)
   - Feature 6: Agree/disagree (`POST /ratings/<user>/<movie>/reaction`)
   - Comprehensive rating management system

4. **Recommendation Service (5004)**
   - Feature 7: Top-rated (`GET /recommendations/top/<user>/`)
   - Feature 8: Friends' unseen (`GET /recommendations/friends/<user>/`)
   - Specialized recommendation algorithms

5. **Newsfeed Service (5005)**
   - Feature 9: Newsfeed (`GET /newsfeed/<user>/`)
   - Aggregates friend activity from Watch History

6. **Movie Service (5006)**
   - Feature 10: Full movie list (`GET /movies/`)
   - Centralized movie data repository

## Service Communication Flow

### `user_service`
- **DB**: Communicates with `user_db` (PostgreSQL) for user data.
- **Used by**:
  - `watch_history_service`
  - `rating_service`
  - `recommendation_service`
  - `newsfeed_service`

---

### `watch_history_service`
- **DB**: Communicates with `watch_db`.
- **External Dependencies**:
  - `user_service` (to get user info/friends)
  - `movie_service` (to fetch movie details)
- **Used by**:
  - `recommendation_service`
  - `newsfeed_service`

---

### `rating_service`
- **DB**: Connects to `rating_db`.
- **External Dependencies**:
  - `user_service` (to get user's friends for social rating features)
  - `movie_service` (for movie info)
- **Used by**:
  - `recommendation_service`

---

### `recommendation_service`
- **Depends on**:
  - `user_service`
  - `watch_history_service`
  - `rating_service`
  - `movie_service`
- **Purpose**: Aggregates user behavior and preferences to generate recommendations.

---

### `newsfeed_service`
- **Depends on**:
  - `user_service`
  - `watch_history_service`
  - `movie_service`
- **Purpose**: Builds a feed of recently watched movies by a user's friends.

---

### `movie_service`
- **Standalone**: No DB but loads movie data from a CSV file.
- **Used by**:
  - `watch_history_service`
  - `rating_service`
  - `recommendation_service`
  - `newsfeed_service`

---

## Database Containers

- `user_db` → used by `user_service`
- `watch_db` → used by `watch_history_service`
- `rating_db` → used by `rating_service`

---

## Microservice Dependencies and Failure Scenarios

### Critical Dependencies:

1. **User Service as Foundation**
   - Required by all other services for user validation
   - Failure impact: Most features become unavailable
   - Mitigation: Implement caching of frequently accessed user data

2. **Movie Service as Data Source**
   - Required for movie validation in Watch and Rating services
   - Failure impact: Cannot log new watches/ratings
   - Mitigation: Bulk load movie IDs at service startup

3. **Watch History for Activity Features**
   - Required by Newsfeed and Recommendation services
   - Failure impact: Newsfeed and friend-based recommendations break
   - Mitigation: Queue-based async processing

### Failure Scenarios:

1. **User Service Outage**
   - Immediate impact: Features 1-10 become partially or completely unavailable
   - Graceful degradation: Services could return cached basic user info

2. **Watch History Service Outage**
   - Impact: Features 3,8,9 fail
   - Recommendation service could fall back to top-rated only (Feature 7)

3. **Rating Service Outage**
   - Impact: Features 4-7 fail
   - Newsfeed (Feature 9) remains operational

## Resiliency Patterns Implemented

1. **Circuit Breakers**
   - Services implement timeout policies for inter-service calls

2. **Health Checks**
   - Docker-compose verifies dependent services are healthy

3. **Bulkheading**
   - Database isolation per service prevents cascading failures

4. **Graceful Degradation**
   - Recommendation service has fallback to random movies when dependencies fail

## Conclusion

The architecture cleanly separates concerns while enabling complex features through coordinated service interactions. The decomposition allows:
- Independent scaling of high-demand features (e.g., Newsfeed vs Recommendations)
- Isolated failure domains
- Clear ownership of data models
- Flexible enhancement of individual features without system-wide changes