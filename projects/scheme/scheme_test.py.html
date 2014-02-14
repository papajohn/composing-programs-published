<html>
<head>
<title>scheme_test.py</title>
<link href="css/assignments.css" rel="stylesheet" type="text/css">
</head>

<body>
<h3>scheme_test.py (<a href="scheme_test.py">plain text</a>)</h3>
<hr>
<pre>
<span style="color: darkred">"""Unit testing framework for the Scheme interpreter.

Usage: python3 scheme_test.py FILE

Interprets FILE as interactive Scheme source code, and compares each line
of printed output from the read-eval-print loop and from any output functions
to an expected output described in a comment.  For example,

(display (+ 2 3))
; expect 5

Differences between printed and expected outputs are printed with line numbers.
"""

</span><span style="color: blue; font-weight: bold">import </span>io
<span style="color: blue; font-weight: bold">import </span>sys
<span style="color: blue; font-weight: bold">from </span>buffer <span style="color: blue; font-weight: bold">import </span>Buffer
<span style="color: blue; font-weight: bold">from </span>scheme <span style="color: blue; font-weight: bold">import </span>read_eval_print_loop<span style="font-weight: bold">, </span>create_global_frame
<span style="color: blue; font-weight: bold">from </span>scheme_tokens <span style="color: blue; font-weight: bold">import </span>tokenize_lines
<span style="color: blue; font-weight: bold">from </span>ucb <span style="color: blue; font-weight: bold">import </span>main

<span style="color: blue; font-weight: bold">def </span>summarize<span style="font-weight: bold">(</span>output<span style="font-weight: bold">, </span>expected_output<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Summarize results of running tests."""
    </span>num_failed<span style="font-weight: bold">, </span>num_expected <span style="font-weight: bold">= </span><span style="color: red">0</span><span style="font-weight: bold">, </span>len<span style="font-weight: bold">(</span>expected_output<span style="font-weight: bold">)

    </span><span style="color: blue; font-weight: bold">def </span>failed<span style="font-weight: bold">(</span>expected<span style="font-weight: bold">, </span>actual<span style="font-weight: bold">, </span>line<span style="font-weight: bold">):
        </span>nonlocal num_failed
        num_failed <span style="font-weight: bold">+= </span><span style="color: red">1
        </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">'test failed at line'</span><span style="font-weight: bold">, </span>line<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">'  expected'</span><span style="font-weight: bold">, </span>expected<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">'   printed'</span><span style="font-weight: bold">, </span>actual<span style="font-weight: bold">)

    </span><span style="color: blue; font-weight: bold">for </span><span style="font-weight: bold">(</span>actual<span style="font-weight: bold">, (</span>expected<span style="font-weight: bold">, </span>line_number<span style="font-weight: bold">)) </span><span style="color: blue; font-weight: bold">in </span>zip<span style="font-weight: bold">(</span>output<span style="font-weight: bold">, </span>expected_output<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">if </span>expected<span style="font-weight: bold">.</span>startswith<span style="font-weight: bold">(</span><span style="color: red">"Error"</span><span style="font-weight: bold">):
            </span><span style="color: blue; font-weight: bold">if not </span>actual<span style="font-weight: bold">.</span>startswith<span style="font-weight: bold">(</span><span style="color: red">"Error"</span><span style="font-weight: bold">):
                </span>failed<span style="font-weight: bold">(</span><span style="color: red">'an error indication'</span><span style="font-weight: bold">, </span>actual<span style="font-weight: bold">, </span>line_number<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">elif </span>actual <span style="font-weight: bold">!= </span>expected<span style="font-weight: bold">:
            </span>failed<span style="font-weight: bold">(</span>expected<span style="font-weight: bold">, </span>actual<span style="font-weight: bold">, </span>line_number<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">'{0} tested; {1} failed.'</span><span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>num_expected<span style="font-weight: bold">, </span>num_failed<span style="font-weight: bold">))

</span>EXPECT_STRING <span style="font-weight: bold">= </span><span style="color: red">'; expect'

</span><span style="color: blue; font-weight: bold">class </span>TestReader<span style="font-weight: bold">:
    </span><span style="color: darkred">"""A TestReader is an iterable that collects test case expected results."""
    </span><span style="color: blue; font-weight: bold">def </span>__init__<span style="font-weight: bold">(</span><span style="color: blue">self</span><span style="font-weight: bold">, </span>lines<span style="font-weight: bold">, </span>stdout<span style="font-weight: bold">):
        </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>lines <span style="font-weight: bold">= </span>lines
        <span style="color: blue">self</span><span style="font-weight: bold">.</span>stdout <span style="font-weight: bold">= </span>stdout
        <span style="color: blue">self</span><span style="font-weight: bold">.</span>last_out_len <span style="font-weight: bold">= </span><span style="color: red">0
        </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>output <span style="font-weight: bold">= []
        </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>expected_output <span style="font-weight: bold">= []
        </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>line_number <span style="font-weight: bold">= </span><span style="color: red">0

    </span><span style="color: blue; font-weight: bold">def </span>__iter__<span style="font-weight: bold">(</span><span style="color: blue">self</span><span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">for </span>line <span style="color: blue; font-weight: bold">in </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>lines<span style="font-weight: bold">:
            </span>line <span style="font-weight: bold">= </span>line<span style="font-weight: bold">.</span>rstrip<span style="font-weight: bold">(</span><span style="color: red">'\n'</span><span style="font-weight: bold">)
            </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>line_number <span style="font-weight: bold">+= </span><span style="color: red">1
            </span><span style="color: blue; font-weight: bold">if </span>line<span style="font-weight: bold">.</span>lstrip<span style="font-weight: bold">().</span>startswith<span style="font-weight: bold">(</span>EXPECT_STRING<span style="font-weight: bold">):
                </span>expected <span style="font-weight: bold">= </span>line<span style="font-weight: bold">.</span>split<span style="font-weight: bold">(</span>EXPECT_STRING<span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">)[</span><span style="color: red">1</span><span style="font-weight: bold">][</span><span style="color: red">1</span><span style="font-weight: bold">:].</span>split<span style="font-weight: bold">(</span><span style="color: red">' ; '</span><span style="font-weight: bold">)
                </span><span style="color: blue; font-weight: bold">for </span>exp <span style="color: blue; font-weight: bold">in </span>expected<span style="font-weight: bold">:
                    </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>expected_output<span style="font-weight: bold">.</span>append<span style="font-weight: bold">((</span>exp<span style="font-weight: bold">, </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>line_number<span style="font-weight: bold">))
                </span>out_lines <span style="font-weight: bold">= </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>stdout<span style="font-weight: bold">.</span>getvalue<span style="font-weight: bold">().</span>split<span style="font-weight: bold">(</span><span style="color: red">'\n'</span><span style="font-weight: bold">)
                </span><span style="color: blue; font-weight: bold">if </span>len<span style="font-weight: bold">(</span>out_lines<span style="font-weight: bold">) &gt; </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>last_out_len<span style="font-weight: bold">:
                    </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>output<span style="font-weight: bold">.</span>extend<span style="font-weight: bold">(</span>out_lines<span style="font-weight: bold">[-</span><span style="color: red">1</span><span style="font-weight: bold">-</span>len<span style="font-weight: bold">(</span>expected<span style="font-weight: bold">):-</span><span style="color: red">1</span><span style="font-weight: bold">])
                </span><span style="color: blue; font-weight: bold">else</span><span style="font-weight: bold">:
                    </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>output<span style="font-weight: bold">.</span>extend<span style="font-weight: bold">([</span><span style="color: red">''</span><span style="font-weight: bold">] * </span>len<span style="font-weight: bold">(</span>expected<span style="font-weight: bold">))
                </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>last_out_len <span style="font-weight: bold">= </span>len<span style="font-weight: bold">(</span>out_lines<span style="font-weight: bold">)
            </span><span style="color: blue; font-weight: bold">yield </span>line
        <span style="color: blue; font-weight: bold">raise </span>EOFError

@main
<span style="color: blue; font-weight: bold">def </span>run_tests<span style="font-weight: bold">(</span>src_file<span style="font-weight: bold">=</span><span style="color: red">'tests.scm'</span><span style="font-weight: bold">):
    </span><span style="color: darkred">"""Run a read-eval loop that reads from src_file and collects outputs."""
    </span>sys<span style="font-weight: bold">.</span>stderr <span style="font-weight: bold">= </span>sys<span style="font-weight: bold">.</span>stdout <span style="font-weight: bold">= </span>io<span style="font-weight: bold">.</span>StringIO<span style="font-weight: bold">() </span><span style="color: green; font-style: italic"># Collect output to stdout and stderr
    </span>reader <span style="font-weight: bold">= </span><span style="color: blue">None
    </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
        </span>reader <span style="font-weight: bold">= </span>TestReader<span style="font-weight: bold">(</span>open<span style="font-weight: bold">(</span>src_file<span style="font-weight: bold">).</span>readlines<span style="font-weight: bold">(), </span>sys<span style="font-weight: bold">.</span>stdout<span style="font-weight: bold">)
        </span>src <span style="font-weight: bold">= </span>Buffer<span style="font-weight: bold">(</span>tokenize_lines<span style="font-weight: bold">(</span>reader<span style="font-weight: bold">))
        </span><span style="color: blue; font-weight: bold">def </span>next_line<span style="font-weight: bold">():
            </span>src<span style="font-weight: bold">.</span>current<span style="font-weight: bold">()
            </span><span style="color: blue; font-weight: bold">return </span>src
        read_eval_print_loop<span style="font-weight: bold">(</span>next_line<span style="font-weight: bold">, </span>create_global_frame<span style="font-weight: bold">())
    </span><span style="color: blue; font-weight: bold">except </span>BaseException as exc<span style="font-weight: bold">:
        </span>sys<span style="font-weight: bold">.</span>stderr <span style="font-weight: bold">= </span>sys<span style="font-weight: bold">.</span>__stderr__
        <span style="color: blue; font-weight: bold">if </span>reader<span style="font-weight: bold">:
            </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">"Tests terminated due to unhandled exception "
                  "after line {0}:\n&gt;&gt;&gt;"</span><span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>reader<span style="font-weight: bold">.</span>line_number<span style="font-weight: bold">),
                  </span>file<span style="font-weight: bold">=</span>sys<span style="font-weight: bold">.</span>stderr<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">raise
    finally</span><span style="font-weight: bold">:
        </span>sys<span style="font-weight: bold">.</span>stdout <span style="font-weight: bold">= </span>sys<span style="font-weight: bold">.</span>__stdout__  <span style="color: green; font-style: italic"># Revert stdout
        </span>sys<span style="font-weight: bold">.</span>stderr <span style="font-weight: bold">= </span>sys<span style="font-weight: bold">.</span>__stderr__  <span style="color: green; font-style: italic"># Revert stderr
    </span>summarize<span style="font-weight: bold">(</span>reader<span style="font-weight: bold">.</span>output<span style="font-weight: bold">, </span>reader<span style="font-weight: bold">.</span>expected_output<span style="font-weight: bold">)
</span>
</pre>
</body>
</html>