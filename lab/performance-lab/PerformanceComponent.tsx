import React, { useState, useEffect } from 'react';
// 1. Anti-pattern: Barrel imports from a potentially heavy library
import { Button, Card, Icon, Input, Text, Spinner, Modal } from './ui-barrel'; 

/**
 * PerformanceComponent
 * 
 * This component intentionally demonstrates several React performance anti-patterns
 * that should be flagged by the 'react-best-practices' skill.
 */
const PerformanceComponent = () => {
  const [userData, setUserData] = useState(null);
  const [userPosts, setUserPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  // 2. Anti-pattern: Waterfall Fetching
  // These effects run sequentially or independently but cause multiple re-renders
  // and delay the final meaningful paint.
  useEffect(() => {
    const fetchUser = async () => {
      const response = await fetch('https://api.example.com/user/1');
      const data = await response.json();
      setUserData(data);
    };
    fetchUser();
  }, []);

  useEffect(() => {
    // This only starts after the first render, and if it depended on userData.id,
    // it would be a classic waterfall. Even here, separate states cause separate renders.
    const fetchPosts = async () => {
      const response = await fetch('https://api.example.com/user/1/posts');
      const data = await response.json();
      setUserPosts(data);
      setLoading(false);
    };
    fetchPosts();
  }, []);

  // 3. Anti-pattern: Inefficient Computation on Every Render
  // This should be wrapped in useMemo
  const sortedPosts = userPosts.sort((a, b) => b.date - a.date);

  if (loading) return <Spinner />;

  return (
    <Card>
      <Text variant="h1">{userData?.name}'s Profile</Text>
      
      {/* 4. Anti-pattern: Passing large inline objects/functions to children */}
      <Button onClick={() => console.log('Clicked!')} style={{ margin: 10, padding: 20 }}>
        Edit Profile
      </Button>

      <section>
        <Text variant="h2">Posts</Text>
        <ul>
          {sortedPosts.map(post => (
            <li key={post.id}>
              <Text>{post.title}</Text>
            </li>
          ))}
        </ul>
      </section>

      {/* 5. Anti-pattern: Missing Lazy Loading for heavy components */}
      {/* HeavyCharts should be dynamic() or React.lazy() */}
      <HeavyCharts data={userPosts} />
    </Card>
  );
};

// Simulated heavy component
const HeavyCharts = ({ data }) => {
  return (
    <div>
      <Text>Complex Data Visualization</Text>
      {/* Imagine a huge D3 or Chart.js implementation here */}
    </div>
  );
};

export default PerformanceComponent;
