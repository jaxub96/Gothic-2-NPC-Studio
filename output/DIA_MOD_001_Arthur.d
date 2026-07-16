instance  Info_Arthur_DISTURB (C_INFO)
{
	npc			= Kdf_404_Arthur;
	condition	= Info_Arthur_DISTURB_Condition;
	information	= Info_Arthur_DISTURB_Info;
	important	= 1;
	permanent	= 0;
};

FUNC int  Info_Arthur_DISTURB_Condition()
{	

	return TRUE;
};
FUNC void  Info_Arthur_DISTURB_Info()
{
	B_WhirlAround	(self, hero);
	AI_Output 		(self, hero,"Info_Arthur_DISTURB_14_01"); //KTO ŒMIE PRZESZKADZAÆ MI W MOICH STUDIACH?
	AI_Output 		(hero, self,"Info_Arthur_DISTURB_15_02"); //Nazywam siê...
	AI_Output 		(self, hero,"Info_Arthur_DISTURB_14_03"); //Nie interesuje mnie twoje imiê. To nieistotne.
	AI_Output 		(self, hero,"Info_Arthur_DISTURB_14_04"); //Liczy siê tylko to, ¿e jesteœ pierwsz¹ osob¹ od wielu lat, której uda³o siê rozwi¹zaæ zagadkê Golemów.
}; 