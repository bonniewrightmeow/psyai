import MedicalDashboard from '@/components/ExpertDashboard';
import { type ConversationCardProps } from '@/components/ConversationCard';
import { useState } from 'react';
import { useLocation } from 'wouter';

export default function ExpertDashboardPage() {
  // In a real app, this would come from auth context or props
  const [userRole] = useState<"nurse" | "doctor">("nurse"); // Default to nurse for demo
  const [location] = useLocation();
  const [conversations] = useState<ConversationCardProps[]>([
    {
      id: 'conv-1',
      title: 'Work-related anxiety support',
      patientName: 'Sarah Johnson',
      status: 'pending_review',
      confidenceScore: 73,
      needsNurseReview: true,
      escalatedToDoctor: false,
      lastMessage: 'I\'ve been feeling really anxious lately, especially about work deadlines. It\'s starting to affect my sleep and I find myself worrying constantly.',
      timestamp: '30 minutes ago',
      messageCount: 2,
    },
    {
      id: 'conv-2',
      title: 'Panic attack management',
      patientName: 'Sarah Johnson',
      status: 'reviewed',
      confidenceScore: 28,
      needsDoctorReview: true,
      escalatedToDoctor: true,
      escalationReason: 'Complex anxiety presentation requires clinical evaluation for potential therapy referral',
      lastMessage: 'I\'ve been having panic attacks at work, especially when deadlines approach. Yesterday I had to leave a meeting because I couldn\'t breathe properly.',
      timestamp: '1 hour ago',
      messageCount: 2,
    },
    {
      id: 'conv-3',
      title: 'General wellness check',
      patientName: 'Michael Chen',
      status: 'active',
      confidenceScore: 95,
      needsNurseReview: false,
      escalatedToDoctor: false,
      lastMessage: 'Just wanted to check in about my mental health routine. Things have been going well overall.',
      timestamp: '2 hours ago',
      messageCount: 8,
    },
    {
      id: 'conv-4', 
      title: 'Depression support',
      patientName: 'Emily Rodriguez',
      status: 'active',
      confidenceScore: 87,
      needsNurseReview: false,
      escalatedToDoctor: false,
      lastMessage: 'I\'ve been following the coping strategies we discussed. Some days are better than others.',
      timestamp: '3 hours ago',
      messageCount: 15,
    },
    {
      id: 'conv-5',
      title: 'Sleep disorder consultation', 
      patientName: 'David Park',
      status: 'reviewed',
      confidenceScore: 92,
      needsNurseReview: false,
      escalatedToDoctor: false,
      lastMessage: 'The sleep hygiene tips have really helped. Getting better rest now.',
      timestamp: '1 day ago',
      messageCount: 12,
    }
  ]);

  const [, setLocation] = useLocation();

  const handleViewConversation = (id: string) => {
    console.log('Opening conversation view for ID:', id);
    setLocation(`/messages/${id}`);
  };

  const handleReviewConversation = (id: string) => {
    console.log('Starting medical review for ID:', id);
    setLocation(`/review/${id}`);
  };

  const handleEscalateToDoctor = (id: string) => {
    console.log('Escalating to doctor for ID:', id);
    setLocation(`/escalation/${id}`);
  };

  // Filter conversations based on current route
  const getFilteredConversations = () => {
    switch (location) {
      case '/cases':
        // Show only cases that need medical attention
        return conversations.filter(conv => 
          conv.status === 'pending_review' || 
          conv.needsNurseReview || 
          conv.needsDoctorReview ||
          conv.escalatedToDoctor
        );
      case '/conversations':
        // Show all conversations, especially active ones
        return conversations.sort((a, b) => {
          // Prioritize active conversations
          if (a.status === 'active' && b.status !== 'active') return -1;
          if (b.status === 'active' && a.status !== 'active') return 1;
          return b.messageCount - a.messageCount; // Then by message count
        });
      default:
        // Dashboard shows everything
        return conversations;
    }
  };

  const getPageTitle = () => {
    switch (location) {
      case '/cases':
        return 'Patient Cases';
      case '/conversations':
        return 'AI Conversations';
      default:
        return userRole === "doctor" ? 'Doctor Dashboard' : 'Nurse Dashboard';
    }
  };

  const getPageSubtitle = () => {
    switch (location) {
      case '/cases':
        return 'Review patient cases requiring medical attention';
      case '/conversations':
        return 'Monitor and manage AI-assisted conversations';
      default:
        return `Welcome back, ${userRole === "doctor" ? "Dr. Sarah Wilson" : "Nurse Jennifer Adams"}`;
    }
  };

  return (
    <MedicalDashboard
      userRole={userRole}
      userName={userRole === "doctor" ? "Dr. Sarah Wilson" : "Nurse Jennifer Adams"}
      conversations={getFilteredConversations()}
      onViewConversation={handleViewConversation}
      onReviewConversation={handleReviewConversation}
      onEscalateToDoctor={handleEscalateToDoctor}
      pageTitle={getPageTitle()}
      pageSubtitle={getPageSubtitle()}
    />
  );
}