<h1>GOLDFINGER</h1>
Created by Ethan Edwards and Collins Senaya

>>
A bot management system. Designed for Forex trading bots but can be used with pretty much any bot/process you want to manage!

<h2>INSTRUCTIONS</h2>
<h3>Manager commands</h3>
<ul>
  <li>help  : Fetches a list of valid commands</li>
  <li>new   : Creates a new bot instance based on a requested file and name</li>
  <li>list  : Lists all currently registered processes and their status</li>
  <li>start : Starts a registered process by name</li>
  <li>kill  : Kills a registered process by name</li>
  <li>quit  : Kills all running processes and quits the program</li>
</ul>

<h3>Client code</h3>
System dependant, see relevant example file

<h3>Notes for Win32</h3>
<ul>
  <li>Threading is unfortunately <i>required</i> for Win32, as signal traps seem to be ineffective at time of writing.</li>
  <li>The <i>entire</i> __init__ function from the example must be copied to any client code, or the manager will be unable to gracefully kill the process.</li>
</ul>

<h2>ROADMAP</h2>
<ul>
  <li>Proper graphical interface</li>
  <li>More control over bots (more verbose status)</li>
</ul>
