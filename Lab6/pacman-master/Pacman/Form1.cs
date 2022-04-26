using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Pacman
{
    public partial class Form1 : Form
    {
        public static GameBoard gameboard = new GameBoard();
        public static Food food = new Food();
        public static Pacman pacman = new Pacman();
        public static Ghost ghost = new Ghost();
        public static Player player = new Player();
        //public static HighScore highscore = new HighScore();
        private static FormElements formelements = new FormElements();
        private static BFSSolver solver = new BFSSolver();

        public Form1()
        {
            InitializeComponent();
            SetupGame(2);
        }

        public void SetupGame(int Level)
        {
            // Create Game Board
            gameboard.CreateBoardImage(this, Level);

            // Create Board Matrix
            Tuple<int, int> PacmanStartCoordinates = gameboard.InitialiseBoardMatrix(Level);

            // Create Player
            player.CreatePlayerDetails(this);
            player.CreateLives(this);

            // Create Form Elements
            formelements.CreateFormElements(this);

            // Create High Score
            //highscore.CreateHighScore(this);

            // Create Food
            food.CreateFoodImages(this);

            // Create Ghosts
            ghost.CreateGhostImage(this);

            // Create Pacman
            pacman.CreatePacmanImage(this, PacmanStartCoordinates.Item1, PacmanStartCoordinates.Item2);
        }

        protected override void OnKeyDown(KeyEventArgs e)
        {
            base.OnKeyDown(e);
            //switch (e.KeyCode)
            //{
            //    case Keys.Up: pacman.nextDirection = 1; pacman.MovePacman(1); break;
            //    case Keys.Right: pacman.nextDirection = 2; pacman.MovePacman(2); break;
            //    case Keys.Down: pacman.nextDirection = 3; pacman.MovePacman(3); break;
            //    case Keys.Left: pacman.nextDirection = 4; pacman.MovePacman(4); break;
            //} 
            playGame();
        }

        protected void playGame()
        {
            var timer = new Timer();
            timer.Tick += delegate

            {
                
                
                
            };

            timer.Interval = 100;
            timer.Start();
            
            //if (pacman.check_direction(2))
            //    all.Add(new Tuple<int, int>(pacman.xCoordinate + 1, pacman.yCoordinate));
            //if (pacman.check_direction(3))
            //    all.Add(new Tuple<int, int>(pacman.xCoordinate, pacman.yCoordinate + 1));
            //if (pacman.check_direction(4))
            //    all.Add(new Tuple<int, int>(pacman.xCoordinate - 1, pacman.yCoordinate));
            //var next = all.Where(a => !visited.Contains(a)).FirstOrDefault();
            //if(next == null)
            //{

            //} else
            //{
            //    pacman.nextDirection()
            //}
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }

    class BFSSolver
    {
        List<Tuple<int, int>> visited = new List<Tuple<int, int>>();

        Stack<Tuple<int, int>> stack = new Stack<Tuple<int, int>>();

        Tuple<int, int> currentPosition = new Tuple<int, int>(0, 0);

        public BFSSolver()
        {
            stack.Push(new Tuple<int, int>(0, 0));
            visited.Add(new Tuple<int, int>(0, 0));
        }

        public int getNextMove(List<int> possibleMoves)
        {
            int nextDirection = -1;
            foreach(int move in possibleMoves)
            {
                var coordinates = toTuple(move);
                if (!visited.Contains(coordinates))
                {
                    nextDirection = move;
                } 
            }

            if(nextDirection != -1)
            {
                //Console.WriteLine(toTuple(nextDirection));
                stack.Push(toTuple(nextDirection));
                this.move(nextDirection);
                return nextDirection;
            } else
            {
                nextDirection = moveBack();
                //Console.WriteLine(toTuple(nextDirection));
                this.move(nextDirection);
                return nextDirection;
            }
        }

        public int moveBack()
        {
            if(stack.Count == 0)
            {
                return 1;
            }
            var currentPosition = stack.Pop();
            var step = stack.Pop();
            stack.Push(step);
            if (currentPosition.Item1 - step.Item1 == 0)
            {
                if (currentPosition.Item2 - step.Item2 == -1)
                    return 3;
                else if (currentPosition.Item2 - step.Item2 == 1)
                    return 1;
            }
            else
            {
                if (currentPosition.Item1 - step.Item1 == -1)
                    return 2;
                else if(currentPosition.Item1 - step.Item1 == 1)
                    return 4;
            }

            return 0;
        }

        void move(int direction)
        {
            Tuple<int, int> cell = toTuple(direction);
       
            currentPosition = cell;

            visited.Add(cell);
            //if(visited.Count > 2)
            //{
            //    visited.RemoveAt(0);
            //}
        }
        

        Tuple<int, int> toTuple(int direction)
        {
            Tuple<int, int> cell = currentPosition;

            switch (direction)
            {
                case 1:
                    cell = new Tuple<int, int>(currentPosition.Item1, currentPosition.Item2 - 1);
                    break;
                case 2:
                    cell = new Tuple<int, int>(currentPosition.Item1 + 1, currentPosition.Item2);
                    break;
                case 3:
                    cell = new Tuple<int, int>(currentPosition.Item1, currentPosition.Item2 + 1);
                    break;
                case 4:
                    cell = new Tuple<int, int>(currentPosition.Item1 - 1, currentPosition.Item2);
                    break;
            }
            return cell;
        }
    }
}
