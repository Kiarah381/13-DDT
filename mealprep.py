interface User {
  email: string;
  name: string;
}
interface Recipe {
  id: string;
  title: string;
  ingredients: string[];
  instructions: string;
  prepTime: string;
  servings: number;
  isFavorite: boolean;
  createdAt: Date;
}
interface MealPlan {
  id: string;
  date: string;
  mealType: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  recipeId?: string;
  customMeal?: string;
  reminder?: Date;
}

interface Notification {
  id: string;
  message: string;
  time: Date;
  read: boolean;
  mealPlanId: string;
}
// ==================== CONTEXT ====================
interface AppContextType {
  user: User | null;
  setUser: (user: User | null) => void;
  recipes: Recipe[];
  setRecipes: React.Dispatch<React.SetStateAction<Recipe[]>>;
  mealPlans: MealPlan[];
  setMealPlans: React.Dispatch<React.SetStateAction<MealPlan[]>>;
  notifications: Notification[];
  setNotifications: React.Dispatch<React.SetStateAction<Notification[]>>;
}
const AppContext = createContext<AppContextType | null>(null);
const useApp = () => {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within AppProvider');
  return context;
};
// ==================== UTILITIES ====================
const generateId = () => Math.random().toString(36).substr(2, 9);
const getWeekDates = (startDate: Date) => {
  const dates = [];
  const start = new Date(startDate);
  start.setDate(start.getDate() - start.getDay());
  for (let i = 0; i < 7; i++) {
    const date = new Date(start);
    date.setDate(start.getDate() + i);
    dates.push(date);
  }
  return dates;
};
const formatDate = (date: Date) => date.toISOString().split('T')[0];
const MEAL_TYPES = ['breakfast', 'lunch', 'dinner', 'snack'] as const;
// ==================== AI RECIPE GENERATOR ====================
const generateAIRecipe = (preferences: string): Recipe => {
  const recipeTemplates = [
    {
      title: 'Mediterranean Quinoa Bowl',
      ingredients: ['1 cup quinoa', '1 cucumber, diced', '1 cup cherry tomatoes', '1/2 cup feta cheese', '1/4 cup olive oil', 'Fresh herbs', 'Lemon juice'],
      instructions: '1. Cook quinoa according to package directions and let cool.\n2. Dice cucumber and halve cherry tomatoes.\n3. Combine quinoa with vegetables in a large bowl.\n4. Crumble feta cheese on top.\n5. Drizzle with olive oil and lemon juice.\n6. Garnish with fresh herbs and serve.',
      prepTime: '25 mins',
      servings: 4,
    },
    {
      title: 'Garlic Butter Salmon',
      ingredients: ['4 salmon fillets', '4 tbsp butter', '4 cloves garlic, minced', '2 tbsp lemon juice', '1 tbsp fresh dill', 'Salt and pepper'],
      instructions: '1. Preheat oven to 400°F (200°C).\n2. Place salmon fillets on a baking sheet.\n3. Melt butter and mix with garlic, lemon juice, and dill.\n4. Brush mixture over salmon fillets.\n5. Season with salt and pepper.\n6. Bake for 12-15 minutes until salmon flakes easily.',
      prepTime: '20 mins',
      servings: 4,
    },
    {
      title: 'Thai Peanut Noodles',
      ingredients: ['8 oz rice noodles', '1/2 cup peanut butter', '3 tbsp soy sauce', '2 tbsp lime juice', '1 tbsp honey', '1 tsp sriracha', 'Green onions', 'Crushed peanuts'],
      instructions: '1. Cook rice noodles according to package directions.\n2. Whisk together peanut butter, soy sauce, lime juice, honey, and sriracha.\n3. Drain noodles and toss with sauce.\n4. Top with sliced green onions and crushed peanuts.\n5. Serve warm or cold.',
      prepTime: '15 mins',
      servings: 4,
    },
    {
      title: 'Veggie-Loaded Frittata',
      ingredients: ['8 eggs', '1/2 cup milk', '1 bell pepper, diced', '1 cup spinach', '1/2 cup cheese', '1/4 cup onion', 'Salt and pepper'],
      instructions: '1. Preheat oven to 375°F (190°C).\n2. Whisk eggs and milk together.\n3. Sauté vegetables until tender.\n4. Pour egg mixture over vegetables in oven-safe skillet.\n5. Sprinkle cheese on top.\n6. Bake for 20-25 minutes until set.',
      prepTime: '35 mins',
      servings: 6,
    },
    {
      title: 'One-Pot Chicken Curry',
      ingredients: ['1 lb chicken breast', '1 can coconut milk', '2 tbsp curry powder', '1 onion', '2 cloves garlic', '1 cup vegetables', 'Rice for serving'],
      instructions: '1. Cut chicken into cubes and season with curry powder.\n2. Sauté onion and garlic until fragrant.\n3. Add chicken and cook until browned.\n4. Pour in coconut milk and add vegetables.\n5. Simmer for 20 minutes.\n6. Serve over rice.',
      prepTime: '35 mins',
      servings: 4,
    },
  ];
  const template = recipeTemplates[Math.floor(Math.random() * recipeTemplates.length)];
  
  return {
    id: generateId(),
    ...template,
    title: preferences ? `${preferences}-Inspired ${template.title}` : template.title,
    isFavorite: false,
    createdAt: new Date(),
  };
};
// ==================== COMPONENTS ====================
// Login Page
const LoginPage: React.FC<{ onLogin: (user: User) => void }> = ({ onLogin }) => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!email || !password || (isSignUp && !name)) {
      setError('Please fill in all fields');
      return;
    }
    if (isSignUp) {
      const users = JSON.parse(localStorage.getItem('prepwise_users') || '{}');
      if (users[email]) {
        setError('Email already registered');
        return;
      }
      users[email] = { password, name };
      localStorage.setItem('prepwise_users', JSON.stringify(users));
    } else {
      const users = JSON.parse(localStorage.getItem('prepwise_users') || '{}');
      if (!users[email] || users[email].password !== password) {
        setError('Invalid email or password');
        return;
      }
      name || setName(users[email].name);
    }
    const user = { email, name: name || JSON.parse(localStorage.getItem('prepwise_users') || '{}')[email]?.name };
    localStorage.setItem('prepwise_current_user', JSON.stringify(user));
    onLogin(user);
  };
  return (
    <div style={styles.loginContainer}>
      <div style={styles.loginCard}>
        <div style={styles.logoContainer}>
          <span style={styles.logoIcon}></span>
          <h1 style={styles.logoText}>PrepWise</h1>
        </div>
        <p style={styles.tagline}>Your intelligent meal planning companion</p>
        
        <form onSubmit={handleSubmit} style={styles.form}>
          <h2 style={styles.formTitle}>{isSignUp ? 'Create Account' : 'Welcome Back'}</h2>
          
          {isSignUp && (
            <input
              type="text"
              placeholder="Full Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={styles.input}
            />
          )}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.input}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
          />
          
          {error && <p style={styles.error}>{error}</p>}
          
          <button type="submit" style={styles.primaryButton}>
            {isSignUp ? 'Sign Up' : 'Log In'}
          </button>
          
          <p style={styles.switchText}>
            {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
            <button
              type="button"
              onClick={() => setIsSignUp(!isSignUp)}
              style={styles.linkButton}
            >
              {isSignUp ? 'Log In' : 'Sign Up'}
            </button>
          </p>
        </form>
      </div>
    </div>
  );
};
// Navigation
const Navigation: React.FC<{ activeTab: string; setActiveTab: (tab: string) => void; onLogout: () => void }> = ({
  activeTab,
  setActiveTab,
  onLogout,
}) => {
  const { notifications, user } = useApp();
  const unreadCount = notifications.filter((n) => !n.read).length;
  const tabs = [
    { id: 'calendar', label: 'Calendar', icon: '📅=' },
    { id: 'recipes', label: 'AI Recipes', icon: '🤖' },
    { id: 'cookbook', label: 'Cookbook', icon: '📖' },
    { id: 'notifications', label: 'Reminders', icon: '🔔' },
  ];
  return (
    <nav style={styles.nav}>
      <div style={styles.navBrand}>
        <span style={styles.navLogo}></span>
        <span style={styles.navTitle}>PrepWise</span>
      </div>
      <div style={styles.navTabs}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              ...styles.navTab,
              ...(activeTab === tab.id ? styles.navTabActive : {}),
            }}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
            {tab.id === 'notifications' && unreadCount > 0 && (
              <span style={styles.badge}>{unreadCount}</span>
            )}
          </button>
        ))}
      </div>
      <div style={styles.navUser}>
        <span style={styles.userName}>{user?.name}</span>
        <button onClick={onLogout} style={styles.logoutButton}>
          Logout
        </button>
      </div>
    </nav>
  );
};
// Weekly Calendar
const WeeklyCalendar: React.FC = () => {
  const { mealPlans, setMealPlans, recipes, setNotifications } = useApp();
  const [currentWeekStart, setCurrentWeekStart] = useState(new Date());
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState<{ date: string; mealType: typeof MEAL_TYPES[number] } | null>(null);
  const [newMeal, setNewMeal] = useState({ recipeId: '', customMeal: '', reminderTime: '' });
  const weekDates = getWeekDates(currentWeekStart);
  const navigateWeek = (direction: number) => {
    const newStart = new Date(currentWeekStart);
    newStart.setDate(newStart.getDate() + direction * 7);
    setCurrentWeekStart(newStart);
  };
  const getMealsForSlot = (date: string, mealType: string) => {
    return mealPlans.filter((mp) => mp.date === date && mp.mealType === mealType);
  };
  const handleAddMeal = () => {
    if (!selectedSlot || (!newMeal.recipeId && !newMeal.customMeal)) return;
    const mealPlan: MealPlan = {
      id: generateId(),
      date: selectedSlot.date,
      mealType: selectedSlot.mealType,
      recipeId: newMeal.recipeId || undefined,
      customMeal: newMeal.customMeal || undefined,
      reminder: newMeal.reminderTime ? new Date(newMeal.reminderTime) : undefined,
    };
    setMealPlans((prev) => [...prev, mealPlan]);
    if (mealPlan.reminder) {
      const recipe = recipes.find((r) => r.id === mealPlan.recipeId);
      const mealName = recipe?.title || mealPlan.customMeal;
      setNotifications((prev) => [
        ...prev,
        {
          id: generateId(),
          message: `Time to prepare: ${mealName} for ${mealPlan.mealType}`,
          time: mealPlan.reminder!,
          read: false,
          mealPlanId: mealPlan.id,
        },
      ]);
    }
    setShowAddModal(false);
    setNewMeal({ recipeId: '', customMeal: '', reminderTime: '' });
    setSelectedSlot(null);
  };
  const deleteMeal = (mealId: string) => {
    setMealPlans((prev) => prev.filter((mp) => mp.id !== mealId));
    setNotifications((prev) => prev.filter((n) => n.mealPlanId !== mealId));
  };
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  return (
    <div style={styles.calendarContainer}>
      <div style={styles.calendarHeader}>
        <button onClick={() => navigateWeek(-1)} style={styles.navArrow}>
          ←
        </button>
        <h2 style={styles.calendarTitle}>
          {weekDates[0].toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
        </h2>
        <button onClick={() => navigateWeek(1)} style={styles.navArrow}>
          →
        </button>
      </div>
      <div style={styles.calendarGrid}>
        <div style={styles.timeColumn}>
          <div style={styles.cornerCell}></div>
          {MEAL_TYPES.map((type) => (
            <div key={type} style={styles.mealTypeLabel}>
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </div>
          ))}
        </div>
        {weekDates.map((date, idx) => (
          <div key={formatDate(date)} style={styles.dayColumn}>
            <div style={styles.dayHeader}>
              <span style={styles.dayName}>{dayNames[idx]}</span>
              <span style={styles.dayNumber}>{date.getDate()}</span>
            </div>
            {MEAL_TYPES.map((mealType) => {
              const meals = getMealsForSlot(formatDate(date), mealType);
              return (
                <div
                  key={mealType}
                  style={styles.mealCell}
                  onClick={() => {
                    setSelectedSlot({ date: formatDate(date), mealType });
                    setShowAddModal(true);
                  }}
                >
                  {meals.map((meal) => {
                    const recipe = recipes.find((r) => r.id === meal.recipeId);
                    return (
                      <div key={meal.id} style={styles.mealCard}>
                        <span style={styles.mealName}>{recipe?.title || meal.customMeal}</span>
                        {meal.reminder && <span style={styles.reminderIcon}>🔔</span>}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteMeal(meal.id);
                          }}
                          style={styles.deleteMealBtn}
                        >
                          ×
                        </button>
                      </div>
                    );
                  })}
                  {meals.length === 0 && <span style={styles.addMealHint}>+ Add</span>}
                </div>
              );
            })}
          </div>
        ))}
      </div>
      {showAddModal && (
        <div style={styles.modalOverlay} onClick={() => setShowAddModal(false)}>
          <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
            <h3 style={styles.modalTitle}>Add Meal</h3>
            <p style={styles.modalSubtitle}>
              {selectedSlot?.mealType} on {selectedSlot?.date}
            </p>
            <div style={styles.formGroup}>
              <label style={styles.label}>Select from Cookbook</label>
              <select
                value={newMeal.recipeId}
                onChange={(e) => setNewMeal({ ...newMeal, recipeId: e.target.value, customMeal: '' })}
                style={styles.select}
              >
                <option value="">-- Choose a recipe --</option>
                {recipes.map((recipe) => (
                  <option key={recipe.id} value={recipe.id}>
                    {recipe.title}
                  </option>
                ))}
              </select>
            </div>
            <div style={styles.divider}>or</div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Custom Meal Name</label>
              <input
                type="text"
                value={newMeal.customMeal}
                onChange={(e) => setNewMeal({ ...newMeal, customMeal: e.target.value, recipeId: '' })}
                placeholder="e.g., Leftover pasta"
                style={styles.input}
              />
            </div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Set Reminder (optional)</label>
              <input
                type="datetime-local"
                value={newMeal.reminderTime}
                onChange={(e) => setNewMeal({ ...newMeal, reminderTime: e.target.value })}
                style={styles.input}
              />
            </div>
            <div style={styles.modalActions}>
              <button onClick={() => setShowAddModal(false)} style={styles.secondaryButton}>
                Cancel
              </button>
              <button onClick={handleAddMeal} style={styles.primaryButton}>
                Add Meal
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
// AI Recipe Generator
const RecipeGenerator: React.FC = () => {
  const { recipes, setRecipes } = useApp();
  const [preferences, setPreferences] = useState('');
  const [generating, setGenerating] = useState(false);
  const [generatedRecipe, setGeneratedRecipe] = useState<Recipe | null>(null);
  const handleGenerate = () => {
    setGenerating(true);
    setTimeout(() => {
      const recipe = generateAIRecipe(preferences);
      setGeneratedRecipe(recipe);
      setGenerating(false);
    }, 1500);
  };
  const saveRecipe = () => {
    if (generatedRecipe) {
      setRecipes((prev) => [...prev, generatedRecipe]);
      setGeneratedRecipe(null);
      setPreferences('');
    }
  };
  return (
    <div style={styles.generatorContainer}>
      <div style={styles.generatorHeader}>
        <h2 style={styles.sectionTitle}>🤖 AI Recipe Generator</h2>
        <p style={styles.sectionSubtitle}>
          Tell me what you're in the mood for, and I'll create a recipe just for you!
        </p>
      </div>
      <div style={styles.generatorInput}>
        <textarea
          value={preferences}
          onChange={(e) => setPreferences(e.target.value)}
          placeholder="Describe what you'd like... (e.g., 'quick healthy dinner', 'Italian pasta', 'vegetarian comfort food')"
          style={styles.textarea}
        />
        <button onClick={handleGenerate} disabled={generating} style={styles.generateButton}>
          {generating ? '✨ Generating...' : '✨ Generate Recipe'}
        </button>
      </div>
      {generatedRecipe && (
        <div style={styles.generatedRecipe}>
          <h3 style={styles.recipeTitle}>{generatedRecipe.title}</h3>
          <div style={styles.recipeMeta}>
            <span>⏱️ {generatedRecipe.prepTime}</span>
            <span>🍽️ {generatedRecipe.servings} servings</span>
          </div>
          <div style={styles.recipeSection}>
            <h4>Ingredients</h4>
            <ul style={styles.ingredientList}>
              {generatedRecipe.ingredients.map((ing, idx) => (
                <li key={idx}>{ing}</li>
              ))}
            </ul>
          </div>
          <div style={styles.recipeSection}>
            <h4>Instructions</h4>
            <p style={styles.instructions}>{generatedRecipe.instructions}</p>
          </div>
          <div style={styles.recipeActions}>
            <button onClick={() => setGeneratedRecipe(null)} style={styles.secondaryButton}>
              Discard
            </button>
            <button onClick={saveRecipe} style={styles.primaryButton}>
              💾 Save to Cookbook
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
// Cookbook
const Cookbook: React.FC = () => {
  const { recipes, setRecipes } = useApp();
  const [showAddForm, setShowAddForm] = useState(false);
  const [filter, setFilter] = useState<'all' | 'favorites'>('all');
  const [expandedRecipe, setExpandedRecipe] = useState<string | null>(null);
  const [newRecipe, setNewRecipe] = useState({
    title: '',
    ingredients: '',
    instructions: '',
    prepTime: '',
    servings: 4,
  });
  const filteredRecipes = filter === 'favorites' ? recipes.filter((r) => r.isFavorite) : recipes;
  const handleAddRecipe = () => {
    if (!newRecipe.title) return;
    const recipe: Recipe = {
      id: generateId(),
      title: newRecipe.title,
      ingredients: newRecipe.ingredients.split('\n').filter((i) => i.trim()),
      instructions: newRecipe.instructions,
      prepTime: newRecipe.prepTime || 'Not specified',
      servings: newRecipe.servings,
      isFavorite: false,
      createdAt: new Date(),
    };
    setRecipes((prev) => [...prev, recipe]);
    setNewRecipe({ title: '', ingredients: '', instructions: '', prepTime: '', servings: 4 });
    setShowAddForm(false);
  };
  const toggleFavorite = (id: string) => {
    setRecipes((prev) => prev.map((r) => (r.id === id ? { ...r, isFavorite: !r.isFavorite } : r)));
  };
  const deleteRecipe = (id: string) => {
    setRecipes((prev) => prev.filter((r) => r.id !== id));
  };
  return (
    <div style={styles.cookbookContainer}>
      <div style={styles.cookbookHeader}>
        <h2 style={styles.sectionTitle}>📖 My Cookbook</h2>
        <div style={styles.cookbookActions}>
          <div style={styles.filterTabs}>
            <button
              onClick={() => setFilter('all')}
              style={{ ...styles.filterTab, ...(filter === 'all' ? styles.filterTabActive : {}) }}
            >
              All Recipes
            </button>
            <button
              onClick={() => setFilter('favorites')}
              style={{ ...styles.filterTab, ...(filter === 'favorites' ? styles.filterTabActive : {}) }}
            >
              ❤️ Favorites
            </button>
          </div>
          <button onClick={() => setShowAddForm(true)} style={styles.addButton}>
            + Add Recipe
          </button>
        </div>
      </div>
      {filteredRecipes.length === 0 ? (
        <div style={styles.emptyState}>
          <p>No recipes yet. Add your first recipe or generate one with AI!</p>
        </div>
      ) : (
        <div style={styles.recipeGrid}>
          {filteredRecipes.map((recipe) => (
            <div key={recipe.id} style={styles.recipeCard}>
              <div style={styles.recipeCardHeader}>
                <h3 style={styles.recipeCardTitle}>{recipe.title}</h3>
                <button onClick={() => toggleFavorite(recipe.id)} style={styles.favoriteBtn}>
                  {recipe.isFavorite ? '❤️' : '🤍'}
                </button>
              </div>
              <div style={styles.recipeCardMeta}>
                <span>⏱️ {recipe.prepTime}</span>
                <span>🍽️ {recipe.servings}</span>
              </div>
              {expandedRecipe === recipe.id ? (
                <div style={styles.recipeCardExpanded}>
                  <h4>Ingredients:</h4>
                  <ul>
                    {recipe.ingredients.map((ing, idx) => (
                      <li key={idx}>{ing}</li>
                    ))}
                  </ul>
                  <h4>Instructions:</h4>
                  <p style={styles.instructionsText}>{recipe.instructions}</p>
                  <button onClick={() => setExpandedRecipe(null)} style={styles.collapseBtn}>
                    Show Less
                  </button>
                </div>
              ) : (
                <button onClick={() => setExpandedRecipe(recipe.id)} style={styles.expandBtn}>
                  View Recipe →
                </button>
              )}
              <button onClick={() => deleteRecipe(recipe.id)} style={styles.deleteBtn}>
                🗑️
              </button>
            </div>
          ))}
        </div>
      )}
      {showAddForm && (
        <div style={styles.modalOverlay} onClick={() => setShowAddForm(false)}>
          <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
            <h3 style={styles.modalTitle}>Add New Recipe</h3>
            <div style={styles.formGroup}>
              <label style={styles.label}>Recipe Title</label>
              <input
                type="text"
                value={newRecipe.title}
                onChange={(e) => setNewRecipe({ ...newRecipe, title: e.target.value })}
                placeholder="e.g., Grandma's Apple Pie"
                style={styles.input}
              />
            </div>
            <div style={styles.formRow}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Prep Time</label>
                <input
                  type="text"
                  value={newRecipe.prepTime}
                  onChange={(e) => setNewRecipe({ ...newRecipe, prepTime: e.target.value })}
                  placeholder="e.g., 30 mins"
                  style={styles.input}
                />
              </div>
              <div style={styles.formGroup}>
                <label style={styles.label}>Servings</label>
                <input
                  type="number"
                  value={newRecipe.servings}
                  onChange={(e) => setNewRecipe({ ...newRecipe, servings: parseInt(e.target.value) || 1 })}
                  style={styles.input}
                />
              </div>
            </div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Ingredients (one per line)</label>
              <textarea
                value={newRecipe.ingredients}
                onChange={(e) => setNewRecipe({ ...newRecipe, ingredients: e.target.value })}
                placeholder="1 cup flour&#10;2 eggs&#10;1/2 cup sugar"
                style={{ ...styles.textarea, height: '100px' }}
              />
            </div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Instructions</label>
              <textarea
                value={newRecipe.instructions}
                onChange={(e) => setNewRecipe({ ...newRecipe, instructions: e.target.value })}
                placeholder="Step-by-step instructions..."
                style={{ ...styles.textarea, height: '120px' }}
              />
            </div>
            <div style={styles.modalActions}>
              <button onClick={() => setShowAddForm(false)} style={styles.secondaryButton}>
                Cancel
              </button>
              <button onClick={handleAddRecipe} style={styles.primaryButton}>
                Save Recipe
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
// Notifications
const Notifications: React.FC = () => {
  const { notifications, setNotifications, mealPlans, recipes } = useApp();
  const sortedNotifications = [...notifications].sort(
    (a, b) => new Date(a.time).getTime() - new Date(b.time).getTime()
  );
  const markAsRead = (id: string) => {
    setNotifications((prev) => prev.map((n) => (n.id === id ? { ...n, read: true } : n)));
  };
  const deleteNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };
  const clearAll = () => {
    setNotifications([]);
  };
  const upcomingNotifications = sortedNotifications.filter((n) => new Date(n.time) >= new Date());
  const pastNotifications = sortedNotifications.filter((n) => new Date(n.time) < new Date());
  return (
    <div style={styles.notificationsContainer}>
      <div style={styles.notificationsHeader}>
        <h2 style={styles.sectionTitle}>🔔 Meal Reminders</h2>
        {notifications.length > 0 && (
          <button onClick={clearAll} style={styles.clearAllBtn}>
            Clear All
          </button>
        )}
      </div>
      {notifications.length === 0 ? (
        <div style={styles.emptyState}>
          <p>No reminders set. Add reminders when planning your meals!</p>
        </div>
      ) : (
        <>
          {upcomingNotifications.length > 0 && (
            <div style={styles.notificationSection}>
              <h3 style={styles.notificationSectionTitle}>Upcoming</h3>
              {upcomingNotifications.map((notification) => (
                <div
                  key={notification.id}
                  style={{
                    ...styles.notificationCard,
                    ...(notification.read ? styles.notificationRead : {}),
                  }}
                  onClick={() => markAsRead(notification.id)}
                >
                  <div style={styles.notificationContent}>
                    <p style={styles.notificationMessage}>{notification.message}</p>
                    <span style={styles.notificationTime}>
                      {new Date(notification.time).toLocaleString()}
                    </span>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteNotification(notification.id);
                    }}
                    style={styles.deleteNotificationBtn}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
          {pastNotifications.length > 0 && (
            <div style={styles.notificationSection}>
              <h3 style={styles.notificationSectionTitle}>Past</h3>
              {pastNotifications.map((notification) => (
                <div
                  key={notification.id}
                  style={{ ...styles.notificationCard, ...styles.notificationPast }}
                >
                  <div style={styles.notificationContent}>
                    <p style={styles.notificationMessage}>{notification.message}</p>
                    <span style={styles.notificationTime}>
                      {new Date(notification.time).toLocaleString()}
                    </span>
                  </div>
                  <button
                    onClick={() => deleteNotification(notification.id)}
                    style={styles.deleteNotificationBtn}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};
// ==================== STYLES ====================
const styles: { [key: string]: React.CSSProperties } = {
  // Login
  loginContainer: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    padding: '20px',
  },
  loginCard: {
    background: 'white',
    borderRadius: '20px',
    padding: '40px',
    width: '100%',
    maxWidth: '400px',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
  },
  logoContainer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
    marginBottom: '10px',
  },
  logoIcon: {
    fontSize: '40px',
  },
  logoText: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#667eea',
    margin: 0,
  },
  tagline: {
    textAlign: 'center',
    color: '#666',
    marginBottom: '30px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
  },
  formTitle: {
    textAlign: 'center',
    margin: '0 0 20px 0',
    color: '#333',
  },
  input: {
    padding: '12px 16px',
    borderRadius: '10px',
    border: '2px solid #eee',
    fontSize: '16px',
    transition: 'border-color 0.2s',
    outline: 'none',
  },
  error: {
    color: '#e74c3c',
    fontSize: '14px',
    margin: 0,
    textAlign: 'center',
  },
  primaryButton: {
    padding: '14px 24px',
    borderRadius: '10px',
    border: 'none',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  secondaryButton: {
    padding: '12px 24px',
    borderRadius: '10px',
    border: '2px solid #667eea',
    background: 'white',
    color: '#667eea',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
  },
  switchText: {
    textAlign: 'center',
    color: '#666',
    fontSize: '14px',
  },
  linkButton: {
    background: 'none',
    border: 'none',
    color: '#667eea',
    fontWeight: 'bold',
    cursor: 'pointer',
    padding: 0,
  },
  // Navigation
  nav: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '15px 30px',
    background: 'white',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  navBrand: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  navLogo: {
    fontSize: '28px',
  },
  navTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#667eea',
  },
  navTabs: {
    display: 'flex',
    gap: '10px',
  },
  navTab: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '10px 20px',
    borderRadius: '10px',
    border: 'none',
    background: 'transparent',
    color: '#666',
    fontSize: '15px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    position: 'relative',
  },
  navTabActive: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
  },
  badge: {
    position: 'absolute',
    top: '-5px',
    right: '-5px',
    background: '#e74c3c',
    color: 'white',
    fontSize: '12px',
    padding: '2px 6px',
    borderRadius: '10px',
  },
  navUser: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  userName: {
    color: '#666',
    fontWeight: '500',
  },
  logoutButton: {
    padding: '8px 16px',
    borderRadius: '8px',
    border: '1px solid #ddd',
    background: 'white',
    color: '#666',
    cursor: 'pointer',
  },
  // Calendar
  calendarContainer: {
    padding: '30px',
  },
  calendarHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '20px',
    marginBottom: '30px',
  },
  calendarTitle: {
    margin: 0,
    fontSize: '24px',
    color: '#333',
    minWidth: '200px',
    textAlign: 'center',
  },
  navArrow: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    border: 'none',
    background: '#f0f0f0',
    fontSize: '20px',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  calendarGrid: {
    display: 'flex',
    gap: '2px',
    background: '#eee',
    borderRadius: '15px',
    overflow: 'hidden',
  },
  timeColumn: {
    width: '100px',
    flexShrink: 0,
  },
  cornerCell: {
    height: '60px',
    background: '#f8f9fa',
  },
  mealTypeLabel: {
    height: '100px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#f8f9fa',
    fontWeight: '600',
    color: '#666',
    fontSize: '14px',
  },
  dayColumn: {
    flex: 1,
    minWidth: '120px',
  },
  dayHeader: {
    height: '60px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
  },
  dayName: {
    fontSize: '12px',
    opacity: 0.8,
  },
  dayNumber: {
    fontSize: '20px',
    fontWeight: 'bold',
  },
  mealCell: {
    height: '100px',
    background: 'white',
    padding: '8px',
    cursor: 'pointer',
    transition: 'background 0.2s',
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
    overflow: 'auto',
  },
  mealCard: {
    background: 'linear-gradient(135deg, #667eea22 0%, #764ba222 100%)',
    padding: '6px 10px',
    borderRadius: '6px',
    fontSize: '12px',
    display: 'flex',
    alignItems: 'center',
    gap: '5px',
    position: 'relative',
  },
  mealName: {
    flex: 1,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  reminderIcon: {
    fontSize: '10px',
  },
  deleteMealBtn: {
    background: 'none',
    border: 'none',
    color: '#999',
    cursor: 'pointer',
    padding: '0 2px',
    fontSize: '14px',
  },
  addMealHint: {
    color: '#ccc',
    fontSize: '12px',
    textAlign: 'center',
    margin: 'auto',
  },
  // Modal
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0,0,0,0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
    padding: '20px',
  },
  modal: {
    background: 'white',
    borderRadius: '20px',
    padding: '30px',
    width: '100%',
    maxWidth: '500px',
    maxHeight: '90vh',
    overflow: 'auto',
  },
  modalTitle: {
    margin: '0 0 10px 0',
    fontSize: '24px',
    color: '#333',
  },
  modalSubtitle: {
    color: '#666',
    marginBottom: '20px',
  },
  modalActions: {
    display: 'flex',
    gap: '15px',
    justifyContent: 'flex-end',
    marginTop: '20px',
  },
  formGroup: {
    marginBottom: '15px',
  },
  formRow: {
    display: 'flex',
    gap: '15px',
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    fontWeight: '600',
    color: '#333',
  },
  select: {
    width: '100%',
    padding: '12px 16px',
    borderRadius: '10px',
    border: '2px solid #eee',
    fontSize: '16px',
    outline: 'none',
  },
  divider: {
    textAlign: 'center',
    color: '#999',
    margin: '15px 0',
    position: 'relative',
  },
  // Recipe Generator
  generatorContainer: {
    padding: '30px',
    maxWidth: '800px',
    margin: '0 auto',
  },
  generatorHeader: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  sectionTitle: {
    fontSize: '28px',
    color: '#333',
    margin: '0 0 10px 0',
  },
  sectionSubtitle: {
    color: '#666',
    fontSize: '16px',
  },
  generatorInput: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
    marginBottom: '30px',
  },
  textarea: {
    padding: '16px',
    borderRadius: '15px',
    border: '2px solid #eee',
    fontSize: '16px',
    resize: 'vertical',
    minHeight: '100px',
    outline: 'none',
    fontFamily: 'inherit',
  },
  generateButton: {
    padding: '16px 32px',
    borderRadius: '15px',
    border: 'none',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    fontSize: '18px',
    fontWeight: 'bold',
    cursor: 'pointer',
    alignSelf: 'center',
  },
  generatedRecipe: {
    background: 'white',
    borderRadius: '20px',
    padding: '30px',
    boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
  },
  recipeTitle: {
    fontSize: '24px',
    color: '#333',
    margin: '0 0 15px 0',
  },
  recipeMeta: {
    display: 'flex',
    gap: '20px',
    color: '#666',
    marginBottom: '20px',
  },
  recipeSection: {
    marginBottom: '20px',
  },
  ingredientList: {
    paddingLeft: '20px',
    lineHeight: '1.8',
  },
  instructions: {
    lineHeight: '1.8',
    whiteSpace: 'pre-line',
  },
  recipeActions: {
    display: 'flex',
    gap: '15px',
    justifyContent: 'flex-end',
    marginTop: '20px',
  },
  // Cookbook
  cookbookContainer: {
    padding: '30px',
  },
  cookbookHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '30px',
    flexWrap: 'wrap',
    gap: '15px',
  },
  cookbookActions: {
    display: 'flex',
    gap: '15px',
    alignItems: 'center',
  },
  filterTabs: {
    display: 'flex',
    background: '#f0f0f0',
    borderRadius: '10px',
    padding: '4px',
  },
  filterTab: {
    padding: '8px 16px',
    borderRadius: '8px',
    border: 'none',
    background: 'transparent',
    cursor: 'pointer',
    fontSize: '14px',
    color: '#666',
  },
  filterTabActive: {
    background: 'white',
    color: '#667eea',
    fontWeight: 'bold',
  },
  addButton: {
    padding: '10px 20px',
    borderRadius: '10px',
    border: 'none',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    fontWeight: 'bold',
    cursor: 'pointer',
  },
  emptyState: {
    textAlign: 'center',
    padding: '60px 20px',
    color: '#999',
  },
  recipeGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '20px',
  },
  recipeCard: {
    background: 'white',
    borderRadius: '15px',
    padding: '20px',
    boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
    position: 'relative',
  },
  recipeCardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '10px',
  },
  recipeCardTitle: {
    margin: 0,
    fontSize: '18px',
    color: '#333',
    paddingRight: '30px',
  },
  favoriteBtn: {
    background: 'none',
    border: 'none',
    fontSize: '20px',
    cursor: 'pointer',
    padding: 0,
  },
  recipeCardMeta: {
    display: 'flex',
    gap: '15px',
    color: '#666',
    fontSize: '14px',
    marginBottom: '15px',
  },
  recipeCardExpanded: {
    borderTop: '1px solid #eee',
    paddingTop: '15px',
    marginTop: '10px',
  },
  instructionsText: {
    whiteSpace: 'pre-line',
    lineHeight: '1.6',
    color: '#555',
  },
  expandBtn: {
    background: 'none',
    border: 'none',
    color: '#667eea',
    fontWeight: 'bold',
    cursor: 'pointer',
    padding: 0,
  },
  collapseBtn: {
    background: 'none',
    border: 'none',
    color: '#667eea',
    fontWeight: 'bold',
    cursor: 'pointer',
    padding: 0,
    marginTop: '15px',
  },
  deleteBtn: {
    position: 'absolute',
    bottom: '15px',
    right: '15px',
    background: 'none',
    border: 'none',
    fontSize: '16px',
    cursor: 'pointer',
    opacity: 0.5,
  },
  // Notifications
  notificationsContainer: {
    padding: '30px',
    maxWidth: '700px',
    margin: '0 auto',
  },
  notificationsHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '30px',
  },
  clearAllBtn: {
    padding: '8px 16px',
    borderRadius: '8px',
    border: '1px solid #ddd',
    background: 'white',
    color: '#666',
    cursor: 'pointer',
  },
  notificationSection: {
    marginBottom: '30px',
  },
  notificationSectionTitle: {
    color: '#666',
    fontSize: '14px',
    textTransform: 'uppercase',
    marginBottom: '15px',
  },
  notificationCard: {
    display: 'flex',
    alignItems: 'center',
    background: 'white',
    borderRadius: '12px',
    padding: '15px 20px',
    marginBottom: '10px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
    cursor: 'pointer',
    borderLeft: '4px solid #667eea',
  },
  notificationRead: {
    opacity: 0.6,
    borderLeftColor: '#ccc',
  },
  notificationPast: {
    opacity: 0.5,
    borderLeftColor: '#ccc',
  },
  notificationContent: {
    flex: 1,
  },
  notificationMessage: {
    margin: '0 0 5px 0',
    color: '#333',
    fontWeight: '500',
  },
  notificationTime: {
    fontSize: '13px',
    color: '#999',
  },
  deleteNotificationBtn: {
    background: 'none',
    border: 'none',
    fontSize: '20px',
    color: '#999',
    cursor: 'pointer',
    padding: '5px 10px',
  },
  // App Container
  appContainer: {
    minHeight: '100vh',
    background: '#f8f9fa',
  },
  mainContent: {
    minHeight: 'calc(100vh - 70px)',
  },
};
// ==================== MAIN APP ====================
export default function PrepWiseApp() {
  const [user, setUser] = useState<User | null>(null);
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [mealPlans, setMealPlans] = useState<MealPlan[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [activeTab, setActiveTab] = useState('calendar');
  const [isLoading, setIsLoading] = useState(true);
  // Load data from localStorage
  useEffect(() => {
    const savedUser = localStorage.getItem('prepwise_current_user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    const savedRecipes = localStorage.getItem('prepwise_recipes');
    if (savedRecipes) {
      setRecipes(JSON.parse(savedRecipes));
    }
    const savedMealPlans = localStorage.getItem('prepwise_mealplans');
    if (savedMealPlans) {
      setMealPlans(JSON.parse(savedMealPlans));
    }
    const savedNotifications = localStorage.getItem('prepwise_notifications');
    if (savedNotifications) {
      setNotifications(JSON.parse(savedNotifications));
    }
    setIsLoading(false);
  }, []);
  // Save data to localStorage
  useEffect(() => {
    if (!isLoading) {
      localStorage.setItem('prepwise_recipes', JSON.stringify(recipes));
    }
  }, [recipes, isLoading]);
  useEffect(() => {
    if (!isLoading) {
      localStorage.setItem('prepwise_mealplans', JSON.stringify(mealPlans));
    }
  }, [mealPlans, isLoading]);
  useEffect(() => {
    if (!isLoading) {
      localStorage.setItem('prepwise_notifications', JSON.stringify(notifications));
    }
  }, [notifications, isLoading]);
  const handleLogin = (loggedInUser: User) => {
    setUser(loggedInUser);
  };
  const handleLogout = () => {
    localStorage.removeItem('prepwise_current_user');
    setUser(null);
  };
  if (isLoading) {
    return (
      <div style={{ ...styles.loginContainer, justifyContent: 'center' }}>
        <div style={{ textAlign: 'center', color: 'white' }}>
          <span style={{ fontSize: '60px' }}>🥗</span>
          <h1>PrepWise</h1>
          <p>Loading...</p>
        </div>
      </div>
    );
  }
  if (!user) {
    return <LoginPage onLogin={handleLogin} />;
  }
  return (
    <AppContext.Provider
      value={{
        user,
        setUser,
        recipes,
        setRecipes,
        mealPlans,
        setMealPlans,
        notifications,
        setNotifications,
      }}
    >
      <div style={styles.appContainer}>
        <Navigation activeTab={activeTab} setActiveTab={setActiveTab} onLogout={handleLogout} />
        <main style={styles.mainContent}>
          {activeTab === 'calendar' && <WeeklyCalendar />}
          {activeTab === 'recipes' && <RecipeGenerator />}
          {activeTab === 'cookbook' && <Cookbook />}
          {activeTab === 'notifications' && <Notifications />}
        </main>
      </div>
    </AppContext.Provider>
  );
}