<html>
<head>
<title>ucb.py</title>
<link href="css/assignments.css" rel="stylesheet" type="text/css">
</head>

<body>
<h3>ucb.py (<a href="ucb.py">plain text</a>)</h3>
<hr>
<pre>
<span style="color: darkred">"""The ucb module contains functions specific to 61A at UC Berkeley."""

</span><span style="color: blue; font-weight: bold">import </span>code
<span style="color: blue; font-weight: bold">import </span>functools
<span style="color: blue; font-weight: bold">import </span>inspect
<span style="color: blue; font-weight: bold">import </span>re
<span style="color: blue; font-weight: bold">import </span>signal
<span style="color: blue; font-weight: bold">import </span>sys


<span style="color: blue; font-weight: bold">def </span>main<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Call fn with command line arguments.  Used as a decorator.

    The main decorator marks the function that starts a program. For example,

    @main
    def my_run_function():
        # function body

    Use this instead of the typical __name__ == "__main__" predicate.
    """
    </span><span style="color: blue; font-weight: bold">if </span>inspect<span style="font-weight: bold">.</span>stack<span style="font-weight: bold">()[</span><span style="color: red">1</span><span style="font-weight: bold">][</span><span style="color: red">0</span><span style="font-weight: bold">].</span>f_locals<span style="font-weight: bold">[</span><span style="color: red">'__name__'</span><span style="font-weight: bold">] == </span><span style="color: red">'__main__'</span><span style="font-weight: bold">:
        </span>args <span style="font-weight: bold">= </span>sys<span style="font-weight: bold">.</span>argv<span style="font-weight: bold">[</span><span style="color: red">1</span><span style="font-weight: bold">:] </span><span style="color: green; font-style: italic"># Discard the script name from command line
        </span>fn<span style="font-weight: bold">(*</span>args<span style="font-weight: bold">) </span><span style="color: green; font-style: italic"># Call the main function
    </span><span style="color: blue; font-weight: bold">return </span>fn


PREFIX <span style="font-weight: bold">= </span><span style="color: red">''
</span><span style="color: blue; font-weight: bold">def </span>trace<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">):
    </span><span style="color: darkred">"""A decorator that prints a function's name, its arguments, and its return
    values each time the function is called. For example,

    @trace
    def compute_something(x, y):
        # function body
    """
    </span>@functools<span style="font-weight: bold">.</span>wraps<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">def </span>wrapped<span style="font-weight: bold">(*</span>args<span style="font-weight: bold">, **</span>kwds<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">global </span>PREFIX
        reprs <span style="font-weight: bold">= [</span>repr<span style="font-weight: bold">(</span>e<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">for </span>e <span style="color: blue; font-weight: bold">in </span>args<span style="font-weight: bold">]
        </span>reprs <span style="font-weight: bold">+= [</span>repr<span style="font-weight: bold">(</span>k<span style="font-weight: bold">) + </span><span style="color: red">'=' </span><span style="font-weight: bold">+ </span>repr<span style="font-weight: bold">(</span>v<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">for </span>k<span style="font-weight: bold">, </span>v <span style="color: blue; font-weight: bold">in </span>kwds<span style="font-weight: bold">.</span>items<span style="font-weight: bold">()]
        </span>log<span style="font-weight: bold">(</span><span style="color: red">'{0}({1})'</span><span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">.</span>__name__<span style="font-weight: bold">, </span><span style="color: red">', '</span><span style="font-weight: bold">.</span>join<span style="font-weight: bold">(</span>reprs<span style="font-weight: bold">)) + </span><span style="color: red">':'</span><span style="font-weight: bold">)
        </span>PREFIX <span style="font-weight: bold">+= </span><span style="color: red">'    '
        </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
            </span>result <span style="font-weight: bold">= </span>fn<span style="font-weight: bold">(*</span>args<span style="font-weight: bold">, **</span>kwds<span style="font-weight: bold">)
            </span>PREFIX <span style="font-weight: bold">= </span>PREFIX<span style="font-weight: bold">[:-</span><span style="color: red">4</span><span style="font-weight: bold">]
        </span><span style="color: blue; font-weight: bold">except </span>Exception as e<span style="font-weight: bold">:
            </span>log<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">.</span>__name__ <span style="font-weight: bold">+ </span><span style="color: red">' exited via exception'</span><span style="font-weight: bold">)
            </span>PREFIX <span style="font-weight: bold">= </span>PREFIX<span style="font-weight: bold">[:-</span><span style="color: red">4</span><span style="font-weight: bold">]
            </span><span style="color: blue; font-weight: bold">raise
        </span><span style="color: green; font-style: italic"># Here, print out the return value.
        </span>log<span style="font-weight: bold">(</span><span style="color: red">'{0}({1}) -&gt; {2}'</span><span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">.</span>__name__<span style="font-weight: bold">, </span><span style="color: red">', '</span><span style="font-weight: bold">.</span>join<span style="font-weight: bold">(</span>reprs<span style="font-weight: bold">), </span>result<span style="font-weight: bold">))
        </span><span style="color: blue; font-weight: bold">return </span>result
    <span style="color: blue; font-weight: bold">return </span>wrapped


<span style="color: blue; font-weight: bold">def </span>log<span style="font-weight: bold">(</span>message<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Print an indented message (used with trace)."""
    </span><span style="color: blue; font-weight: bold">if </span>type<span style="font-weight: bold">(</span>message<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">is not </span>str<span style="font-weight: bold">:
        </span>message <span style="font-weight: bold">= </span>str<span style="font-weight: bold">(</span>message<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span>PREFIX <span style="font-weight: bold">+ </span>re<span style="font-weight: bold">.</span>sub<span style="font-weight: bold">(</span><span style="color: red">'\n'</span><span style="font-weight: bold">, </span><span style="color: red">'\n' </span><span style="font-weight: bold">+ </span>PREFIX<span style="font-weight: bold">, </span>message<span style="font-weight: bold">))


</span><span style="color: blue; font-weight: bold">def </span>log_current_line<span style="font-weight: bold">():
    </span><span style="color: darkred">"""Print information about the current line of code."""
    </span>frame <span style="font-weight: bold">= </span>inspect<span style="font-weight: bold">.</span>stack<span style="font-weight: bold">()[</span><span style="color: red">1</span><span style="font-weight: bold">]
    </span>log<span style="font-weight: bold">(</span><span style="color: red">'Current line: File "{f[1]}", line {f[2]}, in {f[3]}'</span><span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>f<span style="font-weight: bold">=</span>frame<span style="font-weight: bold">))


</span><span style="color: blue; font-weight: bold">def </span>interact<span style="font-weight: bold">(</span>msg<span style="font-weight: bold">=</span><span style="color: blue">None</span><span style="font-weight: bold">):
    </span><span style="color: darkred">"""Start an interactive interpreter session in the current environment.

    On Unix:
      &lt;Control&gt;-D exits the interactive session and returns to normal execution.
    In Windows:
      &lt;Control&gt;-Z &lt;Enter&gt; exists the interactive session and returns to normal
      execution.
    """
    </span><span style="color: green; font-style: italic"># use exception trick to pick up the current frame
    </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">raise </span><span style="color: blue">None
    </span><span style="color: blue; font-weight: bold">except</span><span style="font-weight: bold">:
        </span>frame <span style="font-weight: bold">= </span>sys<span style="font-weight: bold">.</span>exc_info<span style="font-weight: bold">()[</span><span style="color: red">2</span><span style="font-weight: bold">].</span>tb_frame<span style="font-weight: bold">.</span>f_back

    <span style="color: green; font-style: italic"># evaluate commands in current namespace
    </span>namespace <span style="font-weight: bold">= </span>frame<span style="font-weight: bold">.</span>f_globals<span style="font-weight: bold">.</span>copy<span style="font-weight: bold">()
    </span>namespace<span style="font-weight: bold">.</span>update<span style="font-weight: bold">(</span>frame<span style="font-weight: bold">.</span>f_locals<span style="font-weight: bold">)

    </span><span style="color: green; font-style: italic"># exit on interrupt
    </span><span style="color: blue; font-weight: bold">def </span>handler<span style="font-weight: bold">(</span>signum<span style="font-weight: bold">, </span>frame<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">()
        </span>exit<span style="font-weight: bold">(</span><span style="color: red">0</span><span style="font-weight: bold">)
    </span>signal<span style="font-weight: bold">.</span>signal<span style="font-weight: bold">(</span>signal<span style="font-weight: bold">.</span>SIGINT<span style="font-weight: bold">, </span>handler<span style="font-weight: bold">)

    </span><span style="color: blue; font-weight: bold">if not </span>msg<span style="font-weight: bold">:
        </span>_<span style="font-weight: bold">, </span>filename<span style="font-weight: bold">, </span>line<span style="font-weight: bold">, </span>_<span style="font-weight: bold">, </span>_<span style="font-weight: bold">, </span>_ <span style="font-weight: bold">= </span>inspect<span style="font-weight: bold">.</span>stack<span style="font-weight: bold">()[</span><span style="color: red">1</span><span style="font-weight: bold">]
        </span>msg <span style="font-weight: bold">= </span><span style="color: red">'Interacting at File "{0}", line {1} \n'</span><span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>filename<span style="font-weight: bold">, </span>line<span style="font-weight: bold">)
        </span>msg <span style="font-weight: bold">+= </span><span style="color: red">'    Unix:    &lt;Control&gt;-D continues the program; \n'
        </span>msg <span style="font-weight: bold">+= </span><span style="color: red">'    Windows: &lt;Control&gt;-Z &lt;Enter&gt; continues the program; \n'
        </span>msg <span style="font-weight: bold">+= </span><span style="color: red">'    exit() or &lt;Control&gt;-C exits the program'

    </span>code<span style="font-weight: bold">.</span>interact<span style="font-weight: bold">(</span>msg<span style="font-weight: bold">, </span><span style="color: blue">None</span><span style="font-weight: bold">, </span>namespace<span style="font-weight: bold">)
</span>
</pre>
</body>
</html>