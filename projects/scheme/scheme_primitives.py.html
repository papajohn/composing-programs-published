<html>
<head>
<title>scheme_primitives.py</title>
<link href="css/assignments.css" rel="stylesheet" type="text/css">
</head>

<body>
<h3>scheme_primitives.py (<a href="scheme_primitives.py">plain text</a>)</h3>
<hr>
<pre>
<span style="color: darkred">"""This module implements the primitives of the Scheme language."""

</span><span style="color: blue; font-weight: bold">import </span>math
<span style="color: blue; font-weight: bold">import </span>operator
<span style="color: blue; font-weight: bold">import </span>sys
<span style="color: blue; font-weight: bold">from </span>scheme_reader <span style="color: blue; font-weight: bold">import </span>Pair<span style="font-weight: bold">, </span>nil

<span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
    </span><span style="color: blue; font-weight: bold">import </span>turtle
<span style="color: blue; font-weight: bold">except</span><span style="font-weight: bold">:
    </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">"warning: could not import the turtle module."</span><span style="font-weight: bold">, </span>file<span style="font-weight: bold">=</span>sys<span style="font-weight: bold">.</span>stderr<span style="font-weight: bold">)

</span><span style="color: blue; font-weight: bold">class </span>SchemeError<span style="font-weight: bold">(</span>Exception<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Exception indicating an error in a Scheme program."""

</span><span style="color: blue; font-weight: bold">class </span>okay<span style="font-weight: bold">:
    </span><span style="color: darkred">"""Signifies an undefined value."""
    </span><span style="color: blue; font-weight: bold">def </span>__repr__<span style="font-weight: bold">(</span><span style="color: blue">self</span><span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return </span><span style="color: red">"okay"

</span>okay <span style="font-weight: bold">= </span>okay<span style="font-weight: bold">() </span><span style="color: green; font-style: italic"># Assignment hides the okay class; there is only one instance

########################
# Primitive Operations #
########################

</span><span style="color: blue; font-weight: bold">class </span>PrimitiveProcedure<span style="font-weight: bold">:
    </span><span style="color: darkred">"""A Scheme procedure defined as a Python function."""

    </span><span style="color: blue; font-weight: bold">def </span>__init__<span style="font-weight: bold">(</span><span style="color: blue">self</span><span style="font-weight: bold">, </span>fn<span style="font-weight: bold">, </span>use_env<span style="font-weight: bold">=</span><span style="color: blue; font-weight: bold">False</span><span style="font-weight: bold">):
        </span><span style="color: blue">self</span><span style="font-weight: bold">.</span>fn <span style="font-weight: bold">= </span>fn
        <span style="color: blue">self</span><span style="font-weight: bold">.</span>use_env <span style="font-weight: bold">= </span>use_env

    <span style="color: blue; font-weight: bold">def </span>__str__<span style="font-weight: bold">(</span><span style="color: blue">self</span><span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return </span><span style="color: red">'#[primitive]'

</span>_PRIMITIVES <span style="font-weight: bold">= []

</span><span style="color: blue; font-weight: bold">def </span>primitive<span style="font-weight: bold">(*</span>names<span style="font-weight: bold">):
    </span><span style="color: darkred">"""An annotation to convert a Python function into a PrimitiveProcedure."""
    </span><span style="color: blue; font-weight: bold">def </span>add<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">):
        </span>proc <span style="font-weight: bold">= </span>PrimitiveProcedure<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">for </span>name <span style="color: blue; font-weight: bold">in </span>names<span style="font-weight: bold">:
            </span>_PRIMITIVES<span style="font-weight: bold">.</span>append<span style="font-weight: bold">((</span>name<span style="font-weight: bold">,</span>proc<span style="font-weight: bold">))
        </span><span style="color: blue; font-weight: bold">return </span>fn
    <span style="color: blue; font-weight: bold">return </span>add

<span style="color: blue; font-weight: bold">def </span>add_primitives<span style="font-weight: bold">(</span>frame<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Enter bindings in _PRIMITIVES into FRAME, an environment frame."""
    </span><span style="color: blue; font-weight: bold">for </span>name<span style="font-weight: bold">, </span>proc <span style="color: blue; font-weight: bold">in </span>_PRIMITIVES<span style="font-weight: bold">:
        </span>frame<span style="font-weight: bold">.</span>define<span style="font-weight: bold">(</span>name<span style="font-weight: bold">, </span>proc<span style="font-weight: bold">)

</span><span style="color: blue; font-weight: bold">def </span>check_type<span style="font-weight: bold">(</span>val<span style="font-weight: bold">, </span>predicate<span style="font-weight: bold">, </span>k<span style="font-weight: bold">, </span>name<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Returns VAL.  Raises a SchemeError if not PREDICATE(VAL)
    using "argument K of NAME" to describe the offending value."""
    </span><span style="color: blue; font-weight: bold">if not </span>predicate<span style="font-weight: bold">(</span>val<span style="font-weight: bold">):
        </span>msg <span style="font-weight: bold">= </span><span style="color: red">"argument {0} of {1} has wrong type ({2})"
        </span><span style="color: blue; font-weight: bold">raise </span>SchemeError<span style="font-weight: bold">(</span>msg<span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>k<span style="font-weight: bold">, </span>name<span style="font-weight: bold">, </span>type<span style="font-weight: bold">(</span>val<span style="font-weight: bold">).</span>__name__<span style="font-weight: bold">))
    </span><span style="color: blue; font-weight: bold">return </span>val

@primitive<span style="font-weight: bold">(</span><span style="color: red">"boolean?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_booleanp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>x <span style="color: blue; font-weight: bold">is True or </span>x <span style="color: blue; font-weight: bold">is False

def </span>scheme_true<span style="font-weight: bold">(</span>val<span style="font-weight: bold">):
    </span><span style="color: darkred">"""All values in Scheme are true except False."""
    </span><span style="color: blue; font-weight: bold">return </span>val <span style="color: blue; font-weight: bold">is not False

def </span>scheme_false<span style="font-weight: bold">(</span>val<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Only False is false in Scheme."""
    </span><span style="color: blue; font-weight: bold">return </span>val <span style="color: blue; font-weight: bold">is False

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"not"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_not<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return not </span>scheme_true<span style="font-weight: bold">(</span>x<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"eq?"</span><span style="font-weight: bold">, </span><span style="color: red">"equal?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_eqp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>x <span style="font-weight: bold">== </span>y

@primitive<span style="font-weight: bold">(</span><span style="color: red">"pair?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_pairp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>isinstance<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>Pair<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"null?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_nullp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>x <span style="color: blue; font-weight: bold">is </span>nil

@primitive<span style="font-weight: bold">(</span><span style="color: red">"list?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_listp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Return whether x is a well-formed list. Assumes no cycles."""
    </span><span style="color: blue; font-weight: bold">while </span>x <span style="color: blue; font-weight: bold">is not </span>nil<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">if not </span>isinstance<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>Pair<span style="font-weight: bold">):
            </span><span style="color: blue; font-weight: bold">return False
        </span>x <span style="font-weight: bold">= </span>x<span style="font-weight: bold">.</span>second
    <span style="color: blue; font-weight: bold">return True

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"length"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_length<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">if </span>x <span style="color: blue; font-weight: bold">is </span>nil<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span><span style="color: red">0
    </span>check_type<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>scheme_listp<span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">, </span><span style="color: red">'length'</span><span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>len<span style="font-weight: bold">(</span>x<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"cons"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_cons<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>Pair<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"car"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_car<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span>check_type<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>scheme_pairp<span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">, </span><span style="color: red">'car'</span><span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>x<span style="font-weight: bold">.</span>first

@primitive<span style="font-weight: bold">(</span><span style="color: red">"cdr"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_cdr<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span>check_type<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>scheme_pairp<span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">, </span><span style="color: red">'cdr'</span><span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>x<span style="font-weight: bold">.</span>second


@primitive<span style="font-weight: bold">(</span><span style="color: red">"list"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_list<span style="font-weight: bold">(*</span>vals<span style="font-weight: bold">):
    </span>result <span style="font-weight: bold">= </span>nil
    <span style="color: blue; font-weight: bold">for </span>i <span style="color: blue; font-weight: bold">in </span>range<span style="font-weight: bold">(</span>len<span style="font-weight: bold">(</span>vals<span style="font-weight: bold">)-</span><span style="color: red">1</span><span style="font-weight: bold">, -</span><span style="color: red">1</span><span style="font-weight: bold">, -</span><span style="color: red">1</span><span style="font-weight: bold">):
        </span>result <span style="font-weight: bold">= </span>Pair<span style="font-weight: bold">(</span>vals<span style="font-weight: bold">[</span>i<span style="font-weight: bold">], </span>result<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>result

@primitive<span style="font-weight: bold">(</span><span style="color: red">"append"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_append<span style="font-weight: bold">(*</span>vals<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">if </span>len<span style="font-weight: bold">(</span>vals<span style="font-weight: bold">) == </span><span style="color: red">0</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span>nil
    result <span style="font-weight: bold">= </span>vals<span style="font-weight: bold">[-</span><span style="color: red">1</span><span style="font-weight: bold">]
    </span><span style="color: blue; font-weight: bold">for </span>i <span style="color: blue; font-weight: bold">in </span>range<span style="font-weight: bold">(</span>len<span style="font-weight: bold">(</span>vals<span style="font-weight: bold">)-</span><span style="color: red">2</span><span style="font-weight: bold">, -</span><span style="color: red">1</span><span style="font-weight: bold">, -</span><span style="color: red">1</span><span style="font-weight: bold">):
        </span>v <span style="font-weight: bold">= </span>vals<span style="font-weight: bold">[</span>i<span style="font-weight: bold">]
        </span><span style="color: blue; font-weight: bold">if </span>v <span style="color: blue; font-weight: bold">is not </span>nil<span style="font-weight: bold">:
            </span>check_type<span style="font-weight: bold">(</span>v<span style="font-weight: bold">, </span>scheme_pairp<span style="font-weight: bold">, </span>i<span style="font-weight: bold">, </span><span style="color: red">"append"</span><span style="font-weight: bold">)
            </span>r <span style="font-weight: bold">= </span>p <span style="font-weight: bold">= </span>Pair<span style="font-weight: bold">(</span>v<span style="font-weight: bold">.</span>first<span style="font-weight: bold">, </span>result<span style="font-weight: bold">)
            </span>v <span style="font-weight: bold">= </span>v<span style="font-weight: bold">.</span>second
            <span style="color: blue; font-weight: bold">while </span>scheme_pairp<span style="font-weight: bold">(</span>v<span style="font-weight: bold">):
                </span>p<span style="font-weight: bold">.</span>second <span style="font-weight: bold">= </span>Pair<span style="font-weight: bold">(</span>v<span style="font-weight: bold">.</span>first<span style="font-weight: bold">, </span>result<span style="font-weight: bold">)
                </span>p <span style="font-weight: bold">= </span>p<span style="font-weight: bold">.</span>second
                v <span style="font-weight: bold">= </span>v<span style="font-weight: bold">.</span>second
            result <span style="font-weight: bold">= </span>r
    <span style="color: blue; font-weight: bold">return </span>result

@primitive<span style="font-weight: bold">(</span><span style="color: red">"string?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_stringp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>isinstance<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>str<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">and </span>x<span style="font-weight: bold">.</span>startswith<span style="font-weight: bold">(</span><span style="color: red">'"'</span><span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"symbol?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_symbolp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>isinstance<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>str<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">and not </span>scheme_stringp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"number?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_numberp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>isinstance<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>int<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">or </span>isinstance<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>float<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"integer?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_integerp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>isinstance<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>int<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">or </span><span style="font-weight: bold">(</span>scheme_numberp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">and </span>round<span style="font-weight: bold">(</span>x<span style="font-weight: bold">) == </span>x<span style="font-weight: bold">)

</span><span style="color: blue; font-weight: bold">def </span>_check_nums<span style="font-weight: bold">(*</span>vals<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Check that all arguments in VALS are numbers."""
    </span><span style="color: blue; font-weight: bold">for </span>i<span style="font-weight: bold">, </span>v <span style="color: blue; font-weight: bold">in </span>enumerate<span style="font-weight: bold">(</span>vals<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">if not </span>scheme_numberp<span style="font-weight: bold">(</span>v<span style="font-weight: bold">):
            </span>msg <span style="font-weight: bold">= </span><span style="color: red">"operand {0} ({1}) is not a number"
            </span><span style="color: blue; font-weight: bold">raise </span>SchemeError<span style="font-weight: bold">(</span>msg<span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>i<span style="font-weight: bold">, </span>v<span style="font-weight: bold">))

</span><span style="color: blue; font-weight: bold">def </span>_arith<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">, </span>init<span style="font-weight: bold">, </span>vals<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Perform the fn fneration on the number values of VALS, with INIT as
    the value when VALS is empty. Returns the result as a Scheme value."""
    </span>_check_nums<span style="font-weight: bold">(*</span>vals<span style="font-weight: bold">)
    </span>s <span style="font-weight: bold">= </span>init
    <span style="color: blue; font-weight: bold">for </span>val <span style="color: blue; font-weight: bold">in </span>vals<span style="font-weight: bold">:
        </span>s <span style="font-weight: bold">= </span>fn<span style="font-weight: bold">(</span>s<span style="font-weight: bold">, </span>val<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">if </span>round<span style="font-weight: bold">(</span>s<span style="font-weight: bold">) == </span>s<span style="font-weight: bold">:
        </span>s <span style="font-weight: bold">= </span>round<span style="font-weight: bold">(</span>s<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>s

@primitive<span style="font-weight: bold">(</span><span style="color: red">"+"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_add<span style="font-weight: bold">(*</span>vals<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>_arith<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>add<span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">, </span>vals<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"-"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_sub<span style="font-weight: bold">(</span>val0<span style="font-weight: bold">, *</span>vals<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">if </span>len<span style="font-weight: bold">(</span>vals<span style="font-weight: bold">) == </span><span style="color: red">0</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span><span style="font-weight: bold">-</span>val0
    <span style="color: blue; font-weight: bold">return </span>_arith<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>sub<span style="font-weight: bold">, </span>val0<span style="font-weight: bold">, </span>vals<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"*"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_mul<span style="font-weight: bold">(*</span>vals<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>_arith<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>mul<span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">, </span>vals<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"/"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_div<span style="font-weight: bold">(</span>val0<span style="font-weight: bold">, </span>val1<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span>_arith<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>truediv<span style="font-weight: bold">, </span>val0<span style="font-weight: bold">, [</span>val1<span style="font-weight: bold">])
    </span><span style="color: blue; font-weight: bold">except </span>ZeroDivisionError as err<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">raise </span>SchemeError<span style="font-weight: bold">(</span>err<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"quotient"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_quo<span style="font-weight: bold">(</span>val0<span style="font-weight: bold">, </span>val1<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span>_arith<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>floordiv<span style="font-weight: bold">, </span>val0<span style="font-weight: bold">, [</span>val1<span style="font-weight: bold">])
    </span><span style="color: blue; font-weight: bold">except </span>ZeroDivisionError as err<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">raise </span>SchemeError<span style="font-weight: bold">(</span>err<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"modulo"</span><span style="font-weight: bold">, </span><span style="color: red">"remainder"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_modulo<span style="font-weight: bold">(</span>val0<span style="font-weight: bold">, </span>val1<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span>_arith<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>mod<span style="font-weight: bold">, </span>val0<span style="font-weight: bold">, [</span>val1<span style="font-weight: bold">])
    </span><span style="color: blue; font-weight: bold">except </span>ZeroDivisionError as err<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">raise </span>SchemeError<span style="font-weight: bold">(</span>err<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"floor"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_floor<span style="font-weight: bold">(</span>val<span style="font-weight: bold">):
    </span>_check_nums<span style="font-weight: bold">(</span>val<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>math<span style="font-weight: bold">.</span>floor<span style="font-weight: bold">(</span>val<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"ceil"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_ceil<span style="font-weight: bold">(</span>val<span style="font-weight: bold">):
    </span>_check_nums<span style="font-weight: bold">(</span>val<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>math<span style="font-weight: bold">.</span>ceil<span style="font-weight: bold">(</span>val<span style="font-weight: bold">)

</span><span style="color: blue; font-weight: bold">def </span>_numcomp<span style="font-weight: bold">(</span>op<span style="font-weight: bold">, </span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span>_check_nums<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>op<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"="</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_eq<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>_numcomp<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>eq<span style="font-weight: bold">, </span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"&lt;"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_lt<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>_numcomp<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>lt<span style="font-weight: bold">, </span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"&gt;"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_gt<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>_numcomp<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>gt<span style="font-weight: bold">, </span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"&lt;="</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_le<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>_numcomp<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>le<span style="font-weight: bold">, </span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"&gt;="</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_ge<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>_numcomp<span style="font-weight: bold">(</span>operator<span style="font-weight: bold">.</span>ge<span style="font-weight: bold">, </span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"even?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_evenp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span>_check_nums<span style="font-weight: bold">(</span>x<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>x <span style="font-weight: bold">% </span><span style="color: red">2 </span><span style="font-weight: bold">== </span><span style="color: red">0

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"odd?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_oddp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span>_check_nums<span style="font-weight: bold">(</span>x<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>x <span style="font-weight: bold">% </span><span style="color: red">2 </span><span style="font-weight: bold">== </span><span style="color: red">1

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"zero?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_zerop<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span>_check_nums<span style="font-weight: bold">(</span>x<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>x <span style="font-weight: bold">== </span><span style="color: red">0

</span><span style="color: green; font-style: italic">##
## Other operations
##

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"atom?"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_atomp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">if </span>scheme_booleanp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>scheme_numberp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>scheme_symbolp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>scheme_nullp<span style="font-weight: bold">(</span>x<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    return False

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"display"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_display<span style="font-weight: bold">(</span>val<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">if </span>scheme_stringp<span style="font-weight: bold">(</span>val<span style="font-weight: bold">):
        </span>val <span style="font-weight: bold">= </span>eval<span style="font-weight: bold">(</span>val<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span>str<span style="font-weight: bold">(</span>val<span style="font-weight: bold">), </span>end<span style="font-weight: bold">=</span><span style="color: red">""</span><span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"print"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_print<span style="font-weight: bold">(</span>val<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span>str<span style="font-weight: bold">(</span>val<span style="font-weight: bold">))
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"newline"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_newline<span style="font-weight: bold">():
    </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">()
    </span>sys<span style="font-weight: bold">.</span>stdout<span style="font-weight: bold">.</span>flush<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"error"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_error<span style="font-weight: bold">(</span>msg <span style="font-weight: bold">= </span><span style="color: blue">None</span><span style="font-weight: bold">):
    </span>msg <span style="font-weight: bold">= </span><span style="color: red">"" </span><span style="color: blue; font-weight: bold">if </span>msg <span style="color: blue; font-weight: bold">is </span><span style="color: blue">None </span><span style="color: blue; font-weight: bold">else </span>str<span style="font-weight: bold">(</span>msg<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">raise </span>SchemeError<span style="font-weight: bold">(</span>msg<span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"exit"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>scheme_exit<span style="font-weight: bold">():
    </span><span style="color: blue; font-weight: bold">raise </span>EOFError

<span style="color: green; font-style: italic">##
## Turtle graphics (non-standard)
##

</span>_turtle_screen_on <span style="font-weight: bold">= </span><span style="color: blue; font-weight: bold">False

def </span>turtle_screen_on<span style="font-weight: bold">():
    </span><span style="color: blue; font-weight: bold">return </span>_turtle_screen_on

<span style="color: blue; font-weight: bold">def </span>_tscheme_prep<span style="font-weight: bold">():
    </span><span style="color: blue; font-weight: bold">global </span>_turtle_screen_on
    <span style="color: blue; font-weight: bold">if not </span>_turtle_screen_on<span style="font-weight: bold">:
        </span>_turtle_screen_on <span style="font-weight: bold">= </span><span style="color: blue; font-weight: bold">True
        </span>turtle<span style="font-weight: bold">.</span>title<span style="font-weight: bold">(</span><span style="color: red">"Scheme Turtles"</span><span style="font-weight: bold">)
        </span>turtle<span style="font-weight: bold">.</span>mode<span style="font-weight: bold">(</span><span style="color: red">'logo'</span><span style="font-weight: bold">)

</span>@primitive<span style="font-weight: bold">(</span><span style="color: red">"forward"</span><span style="font-weight: bold">, </span><span style="color: red">"fd"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_forward<span style="font-weight: bold">(</span>n<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Move the turtle forward a distance N units on the current heading."""
    </span>_check_nums<span style="font-weight: bold">(</span>n<span style="font-weight: bold">)
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>forward<span style="font-weight: bold">(</span>n<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"backward"</span><span style="font-weight: bold">, </span><span style="color: red">"back"</span><span style="font-weight: bold">, </span><span style="color: red">"bk"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_backward<span style="font-weight: bold">(</span>n<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Move the turtle backward a distance N units on the current heading,
    without changing direction."""
    </span>_check_nums<span style="font-weight: bold">(</span>n<span style="font-weight: bold">)
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>backward<span style="font-weight: bold">(</span>n<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"left"</span><span style="font-weight: bold">, </span><span style="color: red">"lt"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_left<span style="font-weight: bold">(</span>n<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Rotate the turtle's heading N degrees counterclockwise."""
    </span>_check_nums<span style="font-weight: bold">(</span>n<span style="font-weight: bold">)
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>left<span style="font-weight: bold">(</span>n<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"right"</span><span style="font-weight: bold">, </span><span style="color: red">"rt"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_right<span style="font-weight: bold">(</span>n<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Rotate the turtle's heading N degrees clockwise."""
    </span>_check_nums<span style="font-weight: bold">(</span>n<span style="font-weight: bold">)
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>right<span style="font-weight: bold">(</span>n<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"circle"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_circle<span style="font-weight: bold">(</span>r<span style="font-weight: bold">, </span>extent <span style="font-weight: bold">= </span><span style="color: blue">None</span><span style="font-weight: bold">):
    </span><span style="color: darkred">"""Draw a circle with center R units to the left of the turtle (i.e.,
    right if N is negative.  If EXTENT is not None, then draw EXTENT degrees
    of the circle only.  Draws in the clockwise direction if R is negative,
    and otherwise counterclockwise, leaving the turtle facing along the
    arc at its end."""
    </span><span style="color: blue; font-weight: bold">if </span>extent <span style="color: blue; font-weight: bold">is </span><span style="color: blue">None</span><span style="font-weight: bold">:
        </span>_check_nums<span style="font-weight: bold">(</span>r<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">else</span><span style="font-weight: bold">:
        </span>_check_nums<span style="font-weight: bold">(</span>r<span style="font-weight: bold">, </span>extent<span style="font-weight: bold">)
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>circle<span style="font-weight: bold">(</span>r<span style="font-weight: bold">, </span>extent <span style="color: blue; font-weight: bold">and </span>extent<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"setposition"</span><span style="font-weight: bold">, </span><span style="color: red">"setpos"</span><span style="font-weight: bold">, </span><span style="color: red">"goto"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_setposition<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Set turtle's position to (X,Y), heading unchanged."""
    </span>_check_nums<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>setposition<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"setheading"</span><span style="font-weight: bold">, </span><span style="color: red">"seth"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_setheading<span style="font-weight: bold">(</span>h<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Set the turtle's heading H degrees clockwise from north (up)."""
    </span>_check_nums<span style="font-weight: bold">(</span>h<span style="font-weight: bold">)
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>setheading<span style="font-weight: bold">(</span>h<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"penup"</span><span style="font-weight: bold">, </span><span style="color: red">"pu"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_penup<span style="font-weight: bold">():
    </span><span style="color: darkred">"""Raise the pen, so that the turtle does not draw."""
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>penup<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"pendown"</span><span style="font-weight: bold">, </span><span style="color: red">"pd"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_pendown<span style="font-weight: bold">():
    </span><span style="color: darkred">"""Lower the pen, so that the turtle starts drawing."""
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>pendown<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"showturtle"</span><span style="font-weight: bold">, </span><span style="color: red">"st"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_showturtle<span style="font-weight: bold">():
    </span><span style="color: darkred">"""Make turtle visible."""
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>showturtle<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"hideturtle"</span><span style="font-weight: bold">, </span><span style="color: red">"ht"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_hideturtle<span style="font-weight: bold">():
    </span><span style="color: darkred">"""Make turtle visible."""
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>hideturtle<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"clear"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_clear<span style="font-weight: bold">():
    </span><span style="color: darkred">"""Clear the drawing, leaving the turtle unchanged."""
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>clear<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"color"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_color<span style="font-weight: bold">(</span>c<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Set the color to C, a string such as '"red"' or '"#ffc0c0"' (representing
    hexadecimal red, green, and blue values."""
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>check_type<span style="font-weight: bold">(</span>c<span style="font-weight: bold">, </span>scheme_stringp<span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">, </span><span style="color: red">"color"</span><span style="font-weight: bold">)
    </span>turtle<span style="font-weight: bold">.</span>color<span style="font-weight: bold">(</span>eval<span style="font-weight: bold">(</span>c<span style="font-weight: bold">))
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"begin_fill"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_begin_fill<span style="font-weight: bold">():
    </span><span style="color: darkred">"""Start a sequence of moves that outline a shape to be filled."""
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>begin_fill<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"end_fill"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_end_fill<span style="font-weight: bold">():
    </span><span style="color: darkred">"""Fill in shape drawn since last begin_fill."""
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>end_fill<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"exitonclick"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_exitonclick<span style="font-weight: bold">():
    </span><span style="color: darkred">"""Wait for a click on the turtle window, and then close it."""
    </span><span style="color: blue; font-weight: bold">global </span>_turtle_screen_on
    <span style="color: blue; font-weight: bold">if </span>_turtle_screen_on<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">"Close or click on turtle window to complete exit"</span><span style="font-weight: bold">)
        </span>turtle<span style="font-weight: bold">.</span>exitonclick<span style="font-weight: bold">()
        </span>_turtle_screen_on <span style="font-weight: bold">= </span><span style="color: blue; font-weight: bold">False
    return </span>okay

@primitive<span style="font-weight: bold">(</span><span style="color: red">"speed"</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>tscheme_speed<span style="font-weight: bold">(</span>s<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Set the turtle's animation speed as indicated by S (an integer in
    0-10, with 0 indicating no animation (lines draw instantly), and 1-10
    indicating faster and faster movement."""
    </span>check_type<span style="font-weight: bold">(</span>s<span style="font-weight: bold">, </span>scheme_integerp<span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">, </span><span style="color: red">"speed"</span><span style="font-weight: bold">)
    </span>_tscheme_prep<span style="font-weight: bold">()
    </span>turtle<span style="font-weight: bold">.</span>speed<span style="font-weight: bold">(</span>s<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>okay

</pre>
</body>
</html>